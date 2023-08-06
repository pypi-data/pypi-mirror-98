""" Rally Supply Chain support.

Provides management of Rally supply chains

Import example:

>>> from rally import supplyChain
"""
__all__ = [
    'SupplyChainStep',
    'SupplyChainSplit',
    'SupplyChainSequence',
    'SupplyChainCancel',
    'start_new_supply_chain',
    'create_supply_chain_marker',
    'get_supply_chain_metadata',
    'set_supply_chain_metadata'
]
import uuid

from rally import exceptions
from ._session import _getSession, _getAssetByName
from ._context import _rallyContext, _getAssetId, _getJobId

from rally._utils import _datetimeToTimestamp

# TODO We need real examples for working with SupplyChains!!!


def _getAssetBaseId():
    return _rallyContext.get('baseAssetId')


def _getWfRuleId():
    return _rallyContext.get('wfRuleId')


def _getWfId():
    return _rallyContext.get('workflowId')


def _getWfBaseId():
    return _rallyContext.get('workflowBaseId')


def _getWfParentId():
    return _rallyContext.get('workflowParentId')


def _getUserId():
    return _rallyContext.get('userId')


def _getOrgId():
    return _rallyContext.get('orgId')


class SupplyChainStep:
    """ A step in a supply chain. Return an instance of this class for the next step in the supply chain

    :param name: The name of the supply chain step
    :type name: str
    :param dynamic_preset_data: Dynamic preset data passed to the supply chain step. Defaults to `None`
    :type dynamic_preset_data: dict, optional
    :param preset: Overrides the step's preset with the preset of this name. Defaults to `None`
    :type preset: str, optional
    :param priority: Job priority for remainder of the supply chain, defaults to `None` (meaning that the supply chain's
        priority will not be changed). String values must be one of (shown ranked from greatest to least urgency):

        - `urgent`
        - `high`
        - `med_high`
        - `normal`
        - `med_low`
        - `low`
        - `background`
    :type priority:  int or str, optional
    :param supply_chain_deadline: SupplyChain deadline override for remainder of the supply chain. Defaults to `None`
    :type supply_chain_deadline: :py:class:`~datetime.datetime`, optional
    :param step_deadline: SupplyChain deadline override for the supply chain step. Defaults to `None`
    :type step_deadline: :py:class:`~datetime.datetime`, optional
    :param provider_filter: Provider selection filter for the supply chain step. Defaults to `None`
    :type provider_filter: str, optional
    :param retry_policy: Job retry policy for remainder of the supply chain. Must be
       a list of non-negative ints where each int is retry hold time in seconds. Defaults to `None`
    :type retry_policy: list(int), optional
    """

    def __init__(self, name, dynamic_preset_data=None, preset=None, priority=None, supply_chain_deadline=None,
                 step_deadline=None, provider_filter=None, retry_policy=None):
        self.stepName = name
        self.dynamicPresetData = dynamic_preset_data
        self.presetName = preset
        self.workflowJobPriority = _get_job_priority(priority)
        self.movieDeadline = _datetimeToTimestamp(supply_chain_deadline) if supply_chain_deadline else None
        self.movieDeadlineNextStep = _datetimeToTimestamp(step_deadline) if step_deadline else None
        self.providerFilter = provider_filter
        self.workflowJobRetryPolicy = retry_policy

    def _toJson(self):
        retVal = {'stepName': self.stepName}
        for attr in ('stepName', 'dynamicPresetData', 'presetName', 'workflowJobPriority', 'movieDeadline',
                     'movieDeadlineNextStep', 'providerFilter', 'isNewChildWorkflow', 'wfId', 'workflowJobRetryPolicy'):
            if getattr(self, attr, None) is not None:
                retVal[attr] = getattr(self, attr)
        return retVal


class _SupplyChainControlBase:
    def __init__(self):
        self.steps = []
        self.resumeStep = None

    def add_step(self, step):
        if isinstance(step, str):
            step = SupplyChainStep(step)

        if not isinstance(step, SupplyChainStep):
            raise Exception('invalid type for step, {}, expected str or SupplyChainStep'.format(type(step)))

        self.steps.append(step)


# TODO this stuff needs __repr__
class SupplyChainSplit(_SupplyChainControlBase):
    """ An object to represent a split in a supply chain. Return this object to create a split in the supply chain.

    :param resume_step:
    :type resume_step: str or :class:`~rally.supplyChain.SupplyChainStep`
    """
    def __init__(self, resume_step):
        super().__init__()
        if isinstance(resume_step, str):
            resume_step = SupplyChainStep(resume_step)

        if not isinstance(resume_step, SupplyChainStep):
            raise TypeError('invalid type for step, {}, expected str or SupplyChainStep'.format(type(resume_step)))

        self.resumeStep = resume_step

    def add_split(self, step):
        """ Add a split step.

        :param step: Initial supply chain step of a split in the parent supply chain.
        :type step: :class:`~rally.supplyChain.SupplyChainStep`
        """
        self.add_step(step)

    def _toJson(self):
        retVal = []
        for step in self.steps:
            step.isNewChildWorkflow = True
            step.wfId = str(uuid.uuid4())
            retVal.append(step._toJson())

        retVal.append(self.resumeStep._toJson())
        return retVal


class SupplyChainSequence(_SupplyChainControlBase):
    """
    An object to represent a sequence in a supply chain. Return this object to specify a list of next steps
    in the supply chain.

    """
    def __init__(self):
        super().__init__()

    def add_step(self, step):
        """ Add a step the to sequence.

        :param step: Supply chain step
        :type step: :class:`~rally.supplyChain.SupplyChainStep`
        """
        super().add_step(step)

    def _toJson(self):
        return [step._toJson() for step in self.steps]


class SupplyChainCancel:
    """
    Cancels all running and scheduled jobs associated with this supply chain. Supply chain continues at the
    specified SupplyChainStep.

    :param resume_step:
    :type resume_step: str or :class:`~rally.supplyChain.SupplyChainStep`:
    """
    def __init__(self, resume_step):
        if isinstance(resume_step, str):
            resume_step = SupplyChainStep(resume_step)

        if not isinstance(resume_step, SupplyChainStep):
            raise TypeError('invalid type for step, {}, expected str or SupplyChainStep'.format(type(resume_step)))

        self.resumeStep = resume_step

    def _toJson(self):
        return {'cancelAllSubWorkflowsAndResumeAtStep': self.resume_step}


def start_new_supply_chain(asset, step, dynamic_preset_data=None, preset_name=None,
                           supply_chain_job_priority=None, deadline=None,
                           supply_chain_deadline_step_name=None, retry_policy=None,
                           client_resource_id=None):
    """ Start a new supply chain on the specified asset.

    :param asset: Name of the asset. The asset is created if it does not already exist.
    :type asset: str
    :param step: First step to execute in the new supply chain.
    :type step: str or :class:`~rally.supplyChain.SupplyChainStep`
    :param dynamic_preset_data: Dynamic preset data passed to the first step. Defaults to `None` (meaning no preset data
    :type dynamic_preset_data: dict, optional
    :param preset_name: First step preset name override. Defaults to `None`
    :type preset_name: str, optional
    :param supply_chain_job_priority: Job priority override for all steps in the supply chain, defaults to `None`
        (meaning the default priorities are preserved). String values must be one of (shown ranked from greatest to
        least urgency):

        - `urgent`
        - `high`
        - `med_high`
        - `normal`
        - `med_low`
        - `low`
        - `background`
    :type supply_chain_job_priority: int or str, optional
    :param deadline: Supply chain deadline time. Defaults to `None` (meaning this SupplyChain has no
        deadline)
    :type deadline: :py:class:`~datetime.datetime`, optional
    :param supply_chain_deadline_step_name: Name of the first step to execute in another supply chain. This step is
        provided with dynamicPresetData containing the following keys:

        - 'baseWorkflowId'
        - 'workflowId'
        - 'deadlineTime'
        - 'alertTime'

        This new SupplyChain is created and started only when the deadline is reached. It is not created or started
        if the original SupplyChain finishes before the deadline or if the supply-chain_deadline_time and/or the
        supply_chain_deadline_step_name is removed. Note it is possible this new SupplyChain could run after the
        original SupplyChain finishes if the finish time is near the deadline time. Defaults to `None` (meaning no new
        SupplyChain or SupplyChainStep is created upon reaching the deadline).
    :type supply_chain_deadline_step_name: str, optional
    :param retry_policy: Job retry policy override for all steps in the supply chain. Must be
           a list of non-negative ints where each int is retry hold time in seconds. Defaults to `None` (meaning the
           default policy is adhered to).
    :type retry_policy: list(int), optional
    :param client_resource_id: An identifier for the SupplyChain that is meaningful to the creator.  This identifier
        will be by default applied to all jobs in the SupplyChain and to descendent SupplyChains
    :type client_resource_id: str, optional

    Usage:

    >>> start_new_supply_chain('Yeti Corps', 'Vanguard')
    """
    assert isinstance(step, (str, SupplyChainStep)), 'Step argument must be a string or a SupplyChainStep'
    step = step if isinstance(step, str) else step._toJson()
    payload = {'assetName': asset,
               'firstStep': step,
               'dynamicPresetData': dynamic_preset_data,
               'presetName': preset_name,
               'jobPriority': _get_job_priority(supply_chain_job_priority),
               'jobRetryPolicy': retry_policy,
               'deadlineTime': _datetimeToTimestamp(deadline) if deadline else None,
               'deadlineStepName': supply_chain_deadline_step_name,
               'fromWfRuleId': _getWfRuleId(),
               'clientResourceId': client_resource_id}

    if not _getAssetId():
        payload['jobUuidForMovieId'] = _getJobId()

    s = _getSession()
    s.post('v1.0/workflow/new', json=payload)


def create_supply_chain_marker(description, icon, color):
    """
    Create a supply chain marker.

    :param description: Text description to be displayed with the marker, max 50 characters.
    :type description: str
    :param icon: CSS class name for the icon to be used as the marker.
    :type icon: str
    :param color: the icon color, one of:

        - 'pass': equivalent to `green`
        - 'fail': equivalent to `red`
        - a hex value (`#xxxxxx`), or
        - a web color name
    :type color: str

    Usage:

    >>> create_supply_chain_marker('Yeti-Marker', 'fa-thumb-tack', 'burlywood')

    .. seealso::
        `Font Awesome <https://fontawesome.com/icons?d=gallery>`_ documentation for available icons

        `Color keyword <https://developer.mozilla.org/en-US/docs/Web/CSS/color_value>`_ MDN documentation
    """
    description = description or ''

    if len(description) > 50:
        raise ValueError('description must be < 51 characters')
    if not isinstance(color, str):
        raise TypeError('color argument must be a string')

    payload = {
        'success': False if color.lower() == 'fail' else True,
        'desc': description,
        'icon': icon,
        'color': None if color.lower() in ('pass', 'fail') else color,
        'userId': _getUserId(),
        'orgId': _getOrgId(),
        'jobId': _getJobId(),
        'assetId': _getAssetId(),
        'assetBaseId': _getAssetBaseId(),
        'wfRuleId': _getWfRuleId(),
        'wfId': _getWfId(),
        'wfBaseId': _getWfBaseId(),
        'wfParentId': _getWfParentId(),
    }

    s = _getSession()
    s.post('v1.0/workflow/marker', json=payload)


# TODO Cache please
def get_supply_chain_metadata(name=None):
    """ Return a dict containing an Asset's SupplyChain metadata. Raises a :class:`~rally.exceptions.NotFound` if the
    asset does not exist.

    .. warning::
        :func:`rally.supplyChain.get_supply_chain_metadata` is in Alpha Preview and is not considered suitable for
        Production use.  Experimentation in lower environments is encouraged.

    :param name: the asset name, defaults to this Asset
    :type name: str, optional

    Usage:

    >>> get_supply_chain_metadata()
    {'spam': 'eggs', 'yaks': 5}
    """
    assetId = _getAssetByName(name) if name else _getAssetId()
    if not assetId:
        raise exceptions.NotFound(name or 'rally context asset')
    try:
        resp = _getSession().get(f'v2/supplyChainMetadata/{assetId}')
        return resp.json()['data']['attributes']['metadata']
    except exceptions.RallyApiError as err:
        if err.code == 404:
            return {}
        raise


# TODO limit size
def set_supply_chain_metadata(metadata):
    """ Set an Asset's SupplyChain metadata

    .. warning::
        :func:`rally.supplyChain.set_supply_chain_metadata` is in Alpha Preview and is not considered suitable for
        Production use.  Experimentation in lower environments is encouraged.

    :param metadata: metadata to set on the Asset
    :type metadata: dict

    Usage:

    >>> set_supply_chain_metadata({'spam': 'eggs'})
    """
    _getSession().put(f'v1.0/movie/{_getAssetId()}/workflowMetadata2', json={'metadata': metadata})


def _get_job_priority(priority):
    if isinstance(priority, (int, type(None))):
        return priority
    # Normalize str priorities into something the API can understand (PascalCase `PriorityUrgent`)
    if priority.lower() in ('urgent', 'high', 'med_high', 'normal', 'med_low', 'low', 'background'):
        return f'Priority{priority.lower().title().replace("_", "")}'
    # everything else is garbage
    raise ValueError(f'{priority} is not a valid priority')
