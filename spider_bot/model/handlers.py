import logging
from spider_bot.model import common
from spider_bot.model import enums

LOG = logging.getLogger(__name__)


def get_state_handler(data):
    LOG.info('get_state_handler bot:%s' % (common.BOT, ))
    return (enums.NO_ERROR, 1)


def set_action_handler(data):
    LOG.info('set_action_handler:%s' % (common.BOT, ))
    return (enums.NO_ERROR, [])


def enable_notify_handler(data):
    LOG.info('enable_notify_handler:%s' % (common.BOT, ))
    return (enums.NO_ERROR, [])


def register():
    # register handlers
    common.HANDLERS[enums.CMD_GET_STATE] = get_state_handler
    common.HANDLERS[enums.CMD_SET_ACTION] = set_action_handler
    common.HANDLERS[enums.CMD_ENABLE_NOTIFY] = enable_notify_handler
