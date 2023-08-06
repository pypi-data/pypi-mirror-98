"""
A product representing a File in the local filesystem with an optional client,
which allows the file to be retrieved or backed up in remote storage
"""
import json
import shutil
import os
from pathlib import Path
from ploomber.products.Product import Product
from ploomber.placeholders.Placeholder import Placeholder
from reprlib import Repr


class File(Product, os.PathLike):
    """A file (or directory) in the local filesystem

    Parameters
    ----------
    identifier: str or pathlib.Path
        The path to the file (or directory), can contain placeholders
        (e.g. {{placeholder}})
    """
    def __init__(self, identifier, client=None):
        super().__init__(identifier)
        self._client = client
        self._repr = Repr()
        self._repr.maxstring = 40

    def _init_identifier(self, identifier):
        if not isinstance(identifier, (str, Path)):
            raise TypeError('File must be initialized with a str or a '
                            'pathlib.Path')

        return Placeholder(str(identifier))

    @property
    def _path_to_file(self):
        return Path(str(self._identifier))

    @property
    def _path_to_metadata(self):
        name = f'.{self._path_to_file.name}.metadata'
        return self._path_to_file.with_name(name)

    def fetch_metadata(self):
        # to keep compatibility with ploomber<0.10
        old_name = Path(str(self._path_to_file) + '.source')
        if old_name.is_file():
            shutil.move(old_name, self._path_to_metadata)

        empty = dict(timestamp=None, stored_source_code=None)
        # but we have no control over the stored code, it might be missing
        # so we check, we also require the file to exists: even if the
        # .source file exists, missing the actual data file means something
        # if wrong anf the task should run again
        if (self._path_to_metadata.exists() and self._path_to_file.exists()):
            content = self._path_to_metadata.read_text()

            try:
                parsed = json.loads(content)
            except json.JSONDecodeError as e:
                raise ValueError('Error loading JSON metadata '
                                 f'for {self!r} stored at '
                                 f'{str(self._path_to_metadata)!r}') from e
            else:
                # TODO: validate 'stored_source_code', 'timestamp' exist
                return parsed
        else:
            return empty

    def save_metadata(self, metadata):
        self._path_to_metadata.write_text(json.dumps(metadata))

    def _delete_metadata(self):
        if self._path_to_metadata.exists():
            os.remove(str(self._path_to_metadata))

    def exists(self):
        return self._path_to_file.exists()

    def delete(self, force=False):
        # force is not used for this product but it is left for API
        # compatibility
        if self.exists():
            self.logger.debug('Deleting %s', self._path_to_file)
            if self._path_to_file.is_dir():
                shutil.rmtree(str(self._path_to_file))
            else:
                os.remove(str(self._path_to_file))
        else:
            self.logger.debug('%s does not exist ignoring...',
                              self._path_to_file)

    def __repr__(self):
        # do not shorten, we need to process the actual path
        path = Path(self._identifier.best_repr(shorten=False))

        # if absolute, try to show a shorter version, if possible
        if path.is_absolute():
            try:
                path = path.relative_to(Path('.').resolve())
            except ValueError:
                # happens if the path is not a file/folder within the current
                # working directory
                pass

        content = self._repr.repr(str(path))
        return f'{type(self).__name__}({content})'

    @property
    def client(self):
        if self._client is None:
            if self._task is None:
                raise ValueError('Cannot obtain client for this product, '
                                 'the constructor did not receive a client '
                                 'and this product has not been assigned '
                                 'to a DAG yet (cannot look up for clients in'
                                 'dag.clients)')

            self._client = self.task.dag.clients.get(type(self))

        return self._client

    def download(self):
        if (self.client is not None and not self._path_to_metadata.exists()
                and not self._path_to_file.exists()):
            self.logger.info('Downloading %s...', self._path_to_file)
            metadata = str(self._path_to_metadata)
            file_ = str(str(self._path_to_file))

            if self.client._remote_exists(
                    metadata) and self.client._remote_exists(file_):
                self.client.download(metadata)
                self.client.download(file_)

    def upload(self):
        # only upload when we have complete info (product + metadata)
        if (self.client is not None and self._path_to_metadata.exists()
                and self._path_to_file.exists()):
            self.logger.info('Uploading %s...', self._path_to_file)
            self.client.upload(str(self._path_to_metadata))
            self.client.upload(str(self._path_to_file))

    def __fspath__(self):
        """
        Abstract method defined in the os.PathLike interface, enables this
        to work: ``import pandas as pd; pd.read_csv(File('file.csv'))``
        """
        return str(self)
