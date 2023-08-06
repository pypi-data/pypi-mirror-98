""" Rally Notification Support

Most notifications destinations are configured with Notification Presets, typically from the UI.
You can send notifications to those recipients using this module.

Import example:

>>> from rally import notifications
"""
__all__ = [
    'send_notification'
]


from ._session import _getSession
from ._context import _getJobId


# TODO this method should bypass the queue
def send_notification(destination, message, subject='', attributes=None, attachments=None):
    """ Send a notification.  The notification will be queued with Rally's Notification system and sent in the future.

    .. warning::

        :func:`rally.notifications.send_notification` is in Alpha Preview and is not considered suitable for Production use.
        Experimentation in lower environments is encouraged.

    :param destination: name of the notification preset
    :type destination: str
    :param message: notification contents
    :type message: str
    :param subject: notification subject, defaults to empty string
    :type subject: str, optional
    :param attributes: key value pairs to include with the notification, not supported with all notification types,
        defaults to `None`
    :type attributes: dict, optional
    :param attachments: includes the labeled files as notification attachments, not supported with all notification
        types, defaults to `None`
    :type attachments: list(str), optional

    Usage:

    >>> notifications.send_notification('Notify Preset', 'Supply Chain is complete!', subject='Asset: Yak Incorporated')

    Sending Emails:

    >>> notifications.send_notification('rally@sdvi.com', 'Did you know Rally can send emails?', subject='Basic Email')
    """
    _attachments = []
    if attachments:
        for file in attachments:
            if not isinstance(file, str):
                raise TypeError(f'invalid attachment \'{file}\' must be of type string')
            _attachments.append(file)

    if not isinstance(subject, str):
        raise TypeError(f'invalid subject \'{subject}\' must be of type string')

    s = _getSession()
    payload = {
        'destination': destination,
        'text': message,
        'jobUuid': _getJobId(),
        'subject': subject,
        'format': 'raw',
        'attributes': attributes,
        'attachments': _attachments if _attachments else None
    }

    s.post('v1.0/notify/events/new', json=payload)
