""" RallyFile support.

Provides management features for Asset inventory

Import example:

>>> from rally import files
"""
__all__ = [
    'RallyFile',
    'get_inventory',
    'add_inventory',
    'remove_inventory',
    'list_files',
    'read_file',
    'write_file',
    'delete_file',
    'restore_file',
    'get_file_tags',
    'set_file_tags',
    'get_file_metadata'
]

import json
from time import sleep
from urllib.parse import urlparse

from ._context import _getAssetId, _getJobId, _getPriority
from ._session import _getSession, _getAssetByName
from . import exceptions
from ._vendored import requests
from ._utils import _toDatetime
from ._storage import _getStorageLocationFromUrl, _getStoragePartsFromUrl

deleteModes = ('shared_delete', 'forget')
autoJobModes = ('wait', 'nowait', True, False, None)

def _getCspBlobHeaders(url):
    """ Returns the headers for http PUT request to specific storage locations based on url

    :param url: the url needing request headers
    :type url: str
    """
    headersMap = {
        'aliyuncs.com': {'Content-Type': 'binary/octet-stream'},
        'blob.core.windows.net': {'x-ms-blob-type': 'BlockBlob'},
        's3.amazonaws.com': {},
        'storage.googleapis': {'Content-Type': 'binary/octet-stream'},
    }

    for urlPart, header in headersMap.items():
        if urlPart in url:
            return header


class RallyFile:
    """ A file in Rally asset File Inventory.

    :ivar id: (:py:class:`int`) Rally API ID for this file
    :ivar label: (:py:class:`str`) Label used to register this file
    :ivar hashes: (:py:class:`dict`) hashes for this file
    """

    def __init__(self, identifier, **kwargs):
        self.id = identifier
        attrs = kwargs  # todo wtf is this alias
        self.label = attrs['label']
        self.hashes = {k: attrs[k] for k in ('md5', 'sha512', 'sha1') if attrs.get(k)}
        self._tags = attrs['tagList']
        self._instances = attrs.get('instances') or {}

    def __repr__(self):
        return f'{self.__class__.__qualname__} ({self.label})'

    def add_location(self, url):
        """ Register another location for this file

        :param url: the file's URL
        :type url: str

        Usage:

        >>> rally_file.add_location('s3://my-bucket/prefix/file.txt')

        .. warning::
            The caller is responsible for ensuring that the contents of the file at the given location is identical to
            all other registered locations for this :class:`RallyFile`. Rally will treat files at all the locations as
            identical.

        .. note::
            This method does not modify the state of the :class:`RallyFile` instance (e.g. locations does not get
            modified) in-place. If the updated state is needed, lookup the :class:`RallyFile` again with :func:`get_inventory`.

        """
        if not isinstance(url, str):
            raise TypeError('url must be of type str')

        req = {'jobUuid': _getJobId(), 'data': {'id': self.id, 'uri': url, 'label': self.label}}
        _getSession().put(f'v1.0/movie/{_getAssetId()}/files', json=req)

    def remove_location(self, url, mode='shared_delete'):
        """ Removes a copy of this file from a specific location

        :param url: the file's URL
        :type url: str
        :param mode: controls how Rally will remove the file, defaults to `shared_delete`
        :type mode: str, one of :ref:`file-delete-modes`

        Usage:

        >>> rally_file.remove_location(rally_file.locations[0]['url'])

        .. note::

            This method does not modify the state of the :class:`RallyFile` instance (e.g. locations does not get modified)
            in place.  If you need to see the updated state, lookup the :class:`RallyFile` again with :func:`get_inventory`.

        .. seealso::

            :ref:`file-delete-modes`

            :meth:`~rally.files.remove_inventory`

        """
        if mode not in deleteModes:
            raise ValueError(f'mode {mode} unsupported: must be one of {deleteModes}')

        req = {'jobUuid': _getJobId(), 'mode': 'sharedDelete' if mode == 'shared_delete' else mode,
               'data': {'id': self.id, 'uri': url}}
        _getSession().delete(f'v1.0/movie/{_getAssetId()}/files', json=req)

    @property
    def size(self):
        """ Size of this file in bytes. Files with no size return `None` """
        for f in self._instances.values():
            return f.get('size')

    @property
    def tags(self):
        """ List of tags for this file """
        return self._tags

    def add_tags(self, tags):
        """ Add tags to this RallyFile

        :param tags: the name(s) of the Rally tag to add
        :type tags: collection(str)

        Usage:

        >>> files.add_tags(['spam', 'eggs'])

        .. note::

            This method does not modify the state of the :class:`RallyFile` instance.
            If you need to see the updated state, lookup the :class:`RallyFile` again with :func:`get_inventory`.

        """
        _getSession().put(f'v1.0/file/{self.id}/tags', json={'operation': 'add', 'tags': tags})

    def remove_tags(self, tags):
        """ Remove tags from this RallyFile

        :param tags: the name(s) of the Rally tag to remove
        :type tags: collection(str)

        Usage:

        >>> files.remove_tags(['spam'])

        .. note::

            This method does not modify the state of the :class:`RallyFile` instance.
            If you need to see the updated state, lookup the :class:`RallyFile` again with :func:`get_inventory`.
        """
        _getSession().put(f'v1.0/file/{self.id}/tags', json={'operation': 'remove', 'tags': tags})

    @property
    def locations(self):
        """ A list of dicts representing all locations of all the copies of this file

        Location dict attributes:
            - name *(:py:class:`str`)*
            - url *(:py:class:`str`)*
            - rsl *(:py:class:`str`)*
            - status *(:py:class:`str`)*
            - size *(:py:class:`int`)*
            - lastModified *(:py:class:`~datetime.datetime`)*
            - etag *(:py:class:`str`)*
        """

        files = []
        for f in self._instances.values():
            files.append({
                'name': f['name'],
                'url': f['uri'],
                'rsl': f'rsl://{f["storageLocationName"]}/{f["name"]}',
                'status': f['status'],
                'size': f['size'],
                'lastModified': _toDatetime(f['lastModified']),
                'etag': f['hash']
            })
        return files

    def content(self):
        """ Reads the contents of this file

        Usage:

        >>> file = next(get_inventory('Yaks'))
        >>> file.content()
        b'some text'

        Working with encodings other than UTF-8:

        >>> file.content().decode('latin-1')
        'Acción'

        Working with JSON files:

        >>> json.loads(file.content())
        {'myAttribute': 'Yeti', 'Yaks': 3}

        """
        resp = _getSession().get(f'v2/files/{self.id}/content', params={'no-redirect': True})
        file = resp.json()['links']['content']

        # use a different requests.session than the one we use for Rally
        with requests.get(file, timeout=120, stream=True) as r:
            return r.content


# TODO - prevent inventory mutation on other assets
def get_inventory(label=None, tag=None, assetName=None):
    """ Return a `generator iterator <https://docs.python.org/3/glossary.html#term-generator-iterator>`_ of
    :class:`RallyFile` containing items from an Asset's File Inventory matching either the given label **or** the given
    tag. Raises a :class:`~rally.exceptions.NotFound` if the asset does not exist.

    :param label: filter to this label, defaults to None (meaning no filter)
    :type label: str, optional
    :param tag: filter to items with this tag. Default to None (meaning no filter)
    :type tag: str, optional
    :param assetName: the asset name, defaults to this Asset
    :type assetName: str, optional

    Usage

    >>> next(files.get_inventory(label='Yak'))
    RallyFile(Yak)
    """
    filters = {}
    if label:
        filters['label'] = label
    if tag:
        filters['tag'] = tag

    assetId = _getAssetByName(assetName) if assetName else _getAssetId()
    if not assetId:
        raise exceptions.NotFound('asset')
    marker = None

    while True:
        if marker:
            path = marker
            params = None
        else:
            path = f'v2/assets/{assetId}/files'
            params = {'page': '1p100', 'filter': json.dumps(filters)}
        page = _getSession().get(path, params=params).json()
        marker = page['links']['next']

        for f in page['data']:
            yield RallyFile(f['id'], **f['attributes'])

        if not marker:
            return

        sleep(5)


def add_inventory(file, label, tags=None, auto_analyze=None, generate_hash=None):
    """ Adds a file to Asset Inventory

    :param file: the URL, or a list of URLs
    :type file: str, or list(str)
    :param label: the label to use in the Inventory for this file
    :type label: str
    :param tags: tags to apply to this file, maximum 25, defaults to None
    :type tags: list, optional
    :type auto_analyze: str or bool or None
    :param auto_analyze:
        create analyze info for this file by running an :ref:`SDVI Analyze` auto job

        See :ref:`Auto Job Modes` for possible values, defaults to the Silo setting

    :type generate_hash: str or bool or None
    :param generate_hash:
        create hashes for this file by running an :ref:`SDVI Hasher` auto job

        See :ref:`Auto Job Modes` for possible values, defaults to False

    .. note::
        Rally will perform Analyze and Hash creation asynchronously and will not be immediately available
        after inventory registration.  See :ref:`Auto Jobs` for more information.

    Usage:

    >>> files.add_inventory('s3://bucket/file.ext', 'Yak')

    .. warning::
        The caller is responsible for ensuring that the contents of the file at the given location is identical to all
        other registered locations for this :class:`RallyFile`. Rally will treat files at all the locations as identical.
    """
    if not isinstance(file, (str, list)):
        raise ValueError('file must be string, or list')

    if isinstance(file, str) or not hasattr(file, '__iter__'):
        file = (file,)

    if auto_analyze not in autoJobModes:
        raise ValueError(f'auto_analyze must be one of {autoJobModes}')

    if generate_hash not in autoJobModes:
        raise ValueError(f'generate_hash must be one of {autoJobModes}')

    assetId = _getAssetId()

    instances = {}
    for fNum, file in enumerate(file):  # this is dumb...making up fake IDs
        if isinstance(file, str):
            uri = file
        elif isinstance(file, dict):
            uri = file['uri']
        else:
            raise ValueError('must supply a uri')
        instances[fNum] = {'uri': uri}

    tags = set(tags) if tags else set()
    if len(tags) > 25:
        raise ValueError('cannot add more than 25 tags')

    payload = {
        'data': {
            'type': 'files',
            'relationships': {'asset': {'data': {'type': 'assets', 'id': assetId}}},
            'attributes': {
                'label': label,
                'tags': {t: True for t in tags},
                'instances': instances,
                'generateMd5': generate_hash,
                'autoAnalyze': auto_analyze,
                'jobPriority': _getPriority()
            }
        }
    }

    _getSession().post('v2/files', json=payload)


def remove_inventory(rallyfile, mode='shared_delete'):
    """ Remove a file from inventory

    :param rallyfile: the file to remove
    :type rallyfile: RallyFile
    :param mode: controls how Rally will remove the file, defaults to `shared_delete`
    :type mode: str, one of :ref:`file-delete-modes`

    Usage:

    >>> files.remove_inventory(rallyfile)

    .. seealso:: :py:meth:`RallyFile.remove_location`

    """
    if not isinstance(rallyfile, RallyFile):
        raise ValueError('rallyfile must be class RallyFile')

    if mode not in deleteModes:
        raise ValueError(f'mode {mode} unsupported must be one of {deleteModes}')
    req = {'jobUuid': _getJobId(), 'mode': 'sharedDelete' if mode == 'shared_delete' else mode,
           'data': {'id': rallyfile.id, 'uri': '__all__'}}

    # todo we need to save the assetId for this file so we can delete it from the proper asset
    _getSession().delete(f'v1.0/movie/{_getAssetId()}/files', json=req)


# TODO should this be recursive on listings, not sure what it does right now, please report back
#   .. preference is not to recurse
# TODO we might care about the physical size of the file listing due to duplication of text,
#  rick and cecil will talk more later
def list_files(url):
    """ Returns a `generator iterator <https://docs.python.org/3/glossary.html#term-generator-iterator>`_ containing
    URLs of all files at the url provided. Note this is not recursive.

    This function creates a `generator iterator <https://docs.python.org/3/glossary.html#term-generator-iterator>`_ to
    efficently work through the possible large volume of files found in a `StorageLocation`.

    .. warning::
        :func:`rally.files.list_files` is in Alpha Preview and is not considered suitable for Production use.
        Experimentation in lower environments is encouraged.

    :param url: the url to query
    :type url: str

    Usage

    >>> g = files.list_files('rsl://Yeti/MyPrefix')
    >>> next(g)
    's3://Yeti/MyPrefix/file.txt'

    .. warning::

        **Care should be taken when working with new or unfamiliar `StorageLocation`.**

        StorageLocations often have a large number of files contained within them.
    """
    location, directory = _getStoragePartsFromUrl(url)

    req = {'storageLocation': location['attributes']['name']}
    if directory:
        # convert all directories to "foo/"
        prefix = directory.strip('/')
        prefix = f'{prefix}/' if prefix else ''
        req['prefix'] = prefix

    marker = None
    while True:
        if marker:
            req['nextMarker'] = marker
        page = _getSession().get('v1.0/movie/files', json=req).json()
        marker = page.get('next')
        for r in page['results']:
            yield r

        if not marker:
            return

        sleep(5)  # slow down tight loops going back to Rally API


def read_file(url):
    """ Reads a file from a Storage Location.

    :param url: the URL
    :type url: str

    :return: content as bytes

    Usage

    >>> read_file('rsl://location/file.txt')
    b'some text'

    Working with encodings other than UTF-8:

    >>> read_file('rsl://location/file2.txt').decode('latin-1')
    'Acción'

    Working with JSON files:

    >>> json.loads(read_file('rsl://MyMetadataStorage/metadata.json')
    {'a': 'x', 'b': 'y', 'c': 'z'}
    """
    resp = _getSession().get('v2/storageLocations/files/content', params={'url': url, 'no-redirect': True})
    file = resp.json()['links']['content']

    # use a different requests.session than the one we use for Rally
    with requests.get(file, timeout=120, stream=True) as r:
        return r.content


def write_file(url, content):
    """ Writes a file to a Storage Location.

    .. warning::
        :func:`rally.files.write_file` is in Alpha Preview and is not considered suitable for Production use.
        Experimentation in lower environments is encouraged.

    :param url: the URL
    :type url: str
    :param content: the content to be written to the file.
    :type content: bytes, or a :term:`file object`

    Usage:

    >>> files.write_file('rsl://Yeti/neat.txt','some neat text'.encode())
    'rsl://Yeti/neat.txt'

    Working with encodings other than UTF-8:

    >>> files.write_file('rsl://location/file2.txt','Acción'.encode('latin-1'))
    'rsl://MyMetadataStorage/metadata.json'


    Working with JSON files:
    >>> files.write_file('rsl://MyMetadataStorage/metadata.json',json.dumps(metadata).encode())
    'rsl://MyMetadataStorage/metadata.json'
    """
    location, filename = _getStoragePartsFromUrl(url)
    # Unlike Python's standard libraries, the requests library defaults to encoding str with
    # Latin-1 instead of UTF-8 (see https://stackoverflow.com/questions/55887958).
    # Avoid confusion by mandating encoding happens before invoking write_file.
    if isinstance(content, str):
        raise TypeError('content should be bytes or file object; pass my_str.encode() instead of my_str')

    payload = {
        'data': {
            'type': 'storageFileUploadSessions',
            'attributes': {
                'protocol': 'https',
                'sourceName': 'n/a',
                'destinationName': filename,
                'size': requests.utils.super_len(content)
            },
            'relationships': {
                'storageLocation': {'data': {'type': 'storageLocations', 'id': location['id']}}
            }
        }
    }

    resp = _getSession().post('v2/storageFiles/uploadSessions', json=payload)
    transferSpec = resp.json()['data']['attributes']['transferSpecification']
    assert 'url' in transferSpec, 'expecting single part upload session, multipart uploads not supported'

    # use a different requests.session than the one we use for Rally
    resp = requests.put(transferSpec['url'], headers=_getCspBlobHeaders(transferSpec['url']), data=content, timeout=120)
    resp.raise_for_status()


def delete_file(url):
    """ Deletes a file directly from a Storage Location

    .. note::

        If a target URL is actively tracked in the Inventory, the file will be considered "missing" after this operation.

    :param url: the URL
    :type url: str

    Usage

    >>> delete_file('rsl://location/file.txt')
    """
    location = _getStorageLocationFromUrl(url)
    keyname = urlparse(url).path[1:]
    _getSession().delete(f'v2/storageLocations/{location["id"]}/files/{keyname}')


def restore_file(file_url, days, tier=None):
    """ Restores a file from Archive to a Storage Location

    :param file_url: the URL
    :type file_url: str
    :param days: the number of days the file should remain accessible
    :type days: int
    :param tier: the retrieval tier, defaults to None (meaning use the Cloud Provider default)

        .. note::

            Each cloud provider has their own options here, Rally passes the tier string along without modification.
            Visit your Cloud Provider's documentation for possible values

            .. seealso::
                `Amazon S3 Restoring Objects <https://docs.aws.amazon.com/AmazonS3/latest/dev/restoring-objects.html#restoring-objects-retrieval-options>`_
    :type tier: str, optional

    Usage

    >>> files.restore_file('rsl://MyLocation/file.txt',5)
    """
    req = {'url': file_url, 'args': {'days': days, 'tier': tier}}
    _getSession().put(f'v1.0/movie/files/restore', json=req)


def get_file_tags(url):
    """ Returns a :py:class:`dict` containing the object tags for a file in storage

    :param url: the URL
    :type url: str

    Usage

    >>> files.get_tags('s3://my-bucket/prefix/file.txt')
    {'tag1': 'yak', 'tag2': 'yeti'}

    .. seealso::

        `Amazon Object Tagging documentation <https://docs.aws.amazon.com/AmazonS3/latest/dev/object-tagging.html>`_

    """
    location, keyname = _getStoragePartsFromUrl(url)

    req = {'locationName': location['attributes']['name'], 'keyname': keyname}
    resp = _getSession().get(f'v1.0/movie/files/objecttags', json=req)
    return resp.json()


def set_file_tags(url, tags):
    """ Set the object tags on a file in storage

    :param url: the URL
    :type url: str
    :param tags: key-value pairs of tags
    :type tags: dict

    Usage

    >>> files.set_file_tags('s3://my-bucket/prefix/file.txt',{'tag1': 'yak', 'tag2': 'yeti'})

    .. seealso::

        `Amazon Object Tagging documentation <https://docs.aws.amazon.com/AmazonS3/latest/dev/object-tagging.html>`_

    """
    if not isinstance(tags, dict):
        raise ValueError('tags must be a dict')
    if len(tags) > 10:
        raise ValueError('cannot set more than ten (10) tags')
    location, keyname = _getStoragePartsFromUrl(url)

    req = {
        'locationName': location['attributes']['name'],
        'keyname': keyname,
        'tags': tags
    }
    _getSession().put(f'v1.0/movie/files/objecttags', json=req)


def get_file_metadata(url):
    """ Returns a dict containing the cloud provider metadata for a file

    :param url: the URL
    :type url: str

    Usage

    >>> files.get_file_metadata('rsl://MyLocation/file.mxf')
    {'key1': 'value1', 'key2': 'value2'}

    .. seealso::

        `Amazon S3 Object Metadata documentation <https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#object-metadata>`_

    """
    location, keyname = _getStoragePartsFromUrl(url)

    resp = _getSession().get(f'v1.0/movie/files/metadata', json={'locationName': location['attributes']['name'], 'keyname': keyname})
    return resp.json()
