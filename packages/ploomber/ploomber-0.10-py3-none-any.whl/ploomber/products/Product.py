"""
A Product specifies a persistent object in disk such as a file in the local
filesystem or an table in a database. Each Product is uniquely identified,
for example a file can be specified using a absolute path, a table can be
fully specified by specifying a database, a schema and a name. Names
are lazy evaluated, they can be built from templates
"""
import abc
import logging

from ploomber.products.Metadata import Metadata


def _prepare_metadata(metadata):
    return metadata


class Product(abc.ABC):
    """
    Abstract class for all Products

    Attributes
    ----------
    prepare_metadata : callable
        A hook to execute before saving metadata, should include a "metadata"
        parameter and might include "product". "metadata" will be a
        dictionary with the metadata to save, it is not recommended to change
        any of the existing keys but additional key-value pairs might be
        included
    """

    # TODO: previously, File didn't have a client parameter but it does now,
    # it's best to include it here to simplify the constructors in the concrete
    # classes
    def __init__(self, identifier):
        self._identifier = self._init_identifier(identifier)

        if self._identifier is None:
            raise TypeError('_init_identifier must return a value, returned '
                            'None')

        self.task = None
        self.logger = logging.getLogger('{}.{}'.format(__name__,
                                                       type(self).__name__))

        self._outdated_data_dependencies_status = None
        self._outdated_code_dependency_status = None
        # not all products have clients, but they should still have a client
        # property to keep the API consistent
        self._client = None
        self.metadata = Metadata(self)

        self.prepare_metadata = _prepare_metadata

    @property
    def task(self):
        if self._task is None:
            raise ValueError('This product has not been assigned to any Task')

        return self._task

    @property
    def client(self):
        return self._client

    @task.setter
    def task(self, value):
        self._task = value

    def render(self, params, **kwargs):
        """
        Render Product - this will render contents of Templates used as
        identifier for this Product, if a regular string was passed, this
        method has no effect
        """
        self._identifier.render(params, **kwargs)

    def _is_outdated(self, outdated_by_code=True):
        """
        Given current conditions, determine if the Task that holds this
        Product should be executed

        Returns
        -------
        bool
            True if the Task should execute
        """
        # check product...
        p_exists = self.exists()

        # check dependencies only if the product exists
        if p_exists:

            oudated_data = self._outdated_data_dependencies()
            outdated_code = (outdated_by_code
                             and self._outdated_code_dependency())
            run = oudated_data or outdated_code

            if run:
                self.logger.info(
                    'Task "%s" is outdated, it will be executed...',
                    self.task.name)
            else:
                self.logger.info(
                    'Task "%s" is up-to-date, it will be skipped...',
                    self.task.name)

            return run
        else:
            self.logger.info(
                'Product of task "%s" does not exist, it will be executed...',
                self.task.name)
            return True

    def _outdated_data_dependencies(self):
        """
        Determine if the product is outdated by checking upstream timestamps
        """

        if self._outdated_data_dependencies_status is not None:
            self.logger.debug(('Returning cached data dependencies status. '
                               'Outdated? %s'),
                              self._outdated_data_dependencies_status)
            return self._outdated_data_dependencies_status

        def is_outdated(up_prod):
            """
            A task becomes data outdated if an upstream product has a higher
            timestamp or if an upstream product is outdated
            """
            if (self.metadata.timestamp is None
                    or up_prod.metadata.timestamp is None):
                return True
            else:
                return ((up_prod.metadata.timestamp > self.metadata.timestamp)
                        or up_prod._is_outdated())

        outdated = any(
            [is_outdated(up.product) for up in self.task.upstream.values()])

        self._outdated_data_dependencies_status = outdated

        self.logger.debug(('Finished checking data dependencies status. '
                           'Outdated? %s'),
                          self._outdated_data_dependencies_status)

        return self._outdated_data_dependencies_status

    def _outdated_code_dependency(self):
        """
        Determine if the product is outdated by checking the source code that
        it generated it
        """
        if self._outdated_code_dependency_status is not None:
            self.logger.debug(('Returning cached code dependencies status. '
                               'Outdated? %s'),
                              self._outdated_code_dependency_status)
            return self._outdated_code_dependency_status

        outdated, diff = self.task.dag.differ.is_different(
            self.metadata.stored_source_code,
            str(self.task.source),
            extension=self.task.source.extension)

        self._outdated_code_dependency_status = outdated

        self.logger.debug(('Finished checking code status for task "%s" '
                           'Outdated? %s'), self.task.name,
                          self._outdated_code_dependency_status)

        if outdated:
            self.logger.info('Task "%s" has outdated code. Diff:\n%s',
                             self.task.name, diff)

        return self._outdated_code_dependency_status

    def __str__(self):
        return str(self._identifier)

    def __repr__(self):
        # NOTE: this assumes ._identifier has a best_repr property,
        # should we refactor it?
        return '{}({})'.format(
            type(self).__name__, self._identifier.best_repr(shorten=True))

    def __getstate__(self):
        state = self.__dict__.copy()
        # logger is not pickable, so we remove them and build
        # them again in __setstate__
        del state['logger']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.logger = logging.getLogger('{}.{}'.format(__name__,
                                                       type(self).__name__))

    def to_json_serializable(self):
        """Returns a JSON serializable version of this product
        """
        # NOTE: this is used in tasks where only JSON serializable parameters
        # are supported such as NotebookRunner that depends on papermill
        return str(self)

    def __len__(self):
        # MetaProduct return the number of products, this is a single Product
        # hence the 1
        return 1

    # Subclasses must implement the following methods

    @abc.abstractmethod
    def _init_identifier(self, identifier):
        pass  # pragma: no cover

    @abc.abstractmethod
    def fetch_metadata(self):
        pass  # pragma: no cover

    @abc.abstractmethod
    def save_metadata(self, metadata):
        pass  # pragma: no cover

    @abc.abstractmethod
    def exists(self):
        """
        This method returns True if the product exists, it is not part
        of the metadata, so there is no cached status
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def delete(self, force=False):
        """Deletes the product
        """
        pass  # pragma: no cover

    # NOTE: currently optional but there is a conflict with this. metadata
    # defines a delete public method which calls product._delete_metadata
    # but not all products implement this
    def _delete_metadata(self):
        raise NotImplementedError(
            '_delete_metadata not implemented in {}'.format(
                type(self).__name__))

    # download and upload are only relevant for File but we add them to keep
    # the API consistent

    def download(self):
        pass  # pragma: no cover

    def upload(self):
        pass  # pragma: no cover
