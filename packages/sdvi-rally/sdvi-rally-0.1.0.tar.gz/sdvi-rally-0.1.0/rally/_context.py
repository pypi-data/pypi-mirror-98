"""
Note that this file was copied from rally.__init__.py during `commit 795830af28f21f1645b8d7f2f2d4d74f34df382f <https://bitbucket.org/sdvi/monkey/commits/795830af28f21f1645b8d7f2f2d4d74f34df382f>`_
Refer to that commit for git history
"""

import json
import os

from contextlib import suppress


_rallyContext = os.environ.get('rallyContext')
with suppress(Exception):
    _rallyContext = json.loads(_rallyContext)


def _getApiRoot():
    return _rallyContext.get('rallyUrl')


def _getAssetId():
    from ._session import _getAssetByName

    if not _rallyContext.get('assetId') and _rallyContext.get('assetName'):
        _rallyContext['assetId'] = _getAssetByName(_rallyContext.get('assetName'))
    return _rallyContext.get('assetId')


def _getJobId():
    return _rallyContext.get('jobUuid')


def _getPriority():
    return _rallyContext.get('priority')
