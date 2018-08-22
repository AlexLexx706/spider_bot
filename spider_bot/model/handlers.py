import logging
from spider_bot.model import common
from spider_bot.model import enums
import msgpack_numpy as m
m.patch()

LOG = logging.getLogger(__name__)


def get_state(data, **kwargs):
    """handler"""
    # LOG.info('get_state kwargs:%s' % (kwargs, ))
    res = {
        'mat': [
            common.BOT._matrix,
            [
                common.BOT.front_right_leg._matrix,
                common.BOT.front_right_leg.p_0._matrix,
                common.BOT.front_right_leg.p_1._matrix,
                common.BOT.front_right_leg.p_2._matrix,
                common.BOT.front_right_leg.end._matrix],
            [
                common.BOT.front_left_leg._matrix,
                common.BOT.front_left_leg.p_0._matrix,
                common.BOT.front_left_leg.p_1._matrix,
                common.BOT.front_left_leg.p_2._matrix,
                common.BOT.front_left_leg.end._matrix],
            [
                common.BOT.rear_right_leg._matrix,
                common.BOT.rear_right_leg.p_0._matrix,
                common.BOT.rear_right_leg.p_1._matrix,
                common.BOT.rear_right_leg.p_2._matrix,
                common.BOT.rear_right_leg.end._matrix],
            [
                common.BOT.rear_left_leg._matrix,
                common.BOT.rear_left_leg.p_0._matrix,
                common.BOT.rear_left_leg.p_1._matrix,
                common.BOT.rear_left_leg.p_2._matrix,
                common.BOT.rear_left_leg.end._matrix]],
        'action': common.BOT.action
    }
    return (enums.NO_ERROR, res)


def set_action(action, **kwargs):
    LOG.info('set_action')
    common.BOT.action = action
    return (enums.NO_ERROR, [])


def add_notify(port, **kwargs):
    LOG.info('add_notify port:%s, addr:%s' % (port, kwargs['addr']))
    common.NOTIFY.add((kwargs['addr'][0], port))


def rm_notify(port, **kwargs):
    LOG.info('rm_notify port:%s, addr:%s' % (port, kwargs['addr']))
    common.NOTIFY.remove((kwargs['addr'][0], port))


def register():
    # register handlers
    common.HANDLERS[enums.CMD_GET_STATE] = get_state
    common.HANDLERS[enums.CMD_SET_ACTION] = set_action
    common.HANDLERS[enums.CMD_ADD_NOTIFY] = add_notify
    common.HANDLERS[enums.CMD_RM_NOTIFY] = rm_notify
