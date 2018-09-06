import ctypes

CMD_GET_STATE = 0
CMD_SET_ACTION = 1
CMD_ADD_NOTIFY = 2
CMD_RM_NOTIFY = 3

NO_ERROR = 0
WRONG_COMMAND = 1
UNKNOWN_ERROR = 2


NOT_MOVE = 0
MOVE_FORWARD = 1
MOVE_BACKWARD = 2
ROTATE_LEFT = 3
ROTATE_RIGHT = 4


# #############################################
class Header(ctypes.Structure):
    _fields_ = (
        ('cmd', ctypes.c_int),
        ('size', ctypes.c_uint))


class ResHeader(ctypes.Structure):
    _fields_ = (
        ('header', Header),
        ('error', ctypes.c_int))
    _pack_ = 1


class LegDesc(ctypes.Structure):
    _fields_ = (
        ('pos', ctypes.c_float * 3),
        ('shoulder_offset', ctypes.c_float),
        ('shoulder_lenght', ctypes.c_float),
        ('forearm_lenght', ctypes.c_float),
        ('end', ctypes.c_float * 3),)
    _pack_ = 1


class GetStateRes(ctypes.Structure):
    _fields_ = (
        ('header', ResHeader),
        ('body_mat', ctypes.c_float * 16),
        ('front_right_leg', LegDesc),
        ('front_left_leg', LegDesc),
        ('rear_right_leg', LegDesc),
        ('rear_left_leg', LegDesc),
        ('action', ctypes.c_int))
    _pack_ = 1


class SetActionCmd(ctypes.Structure):
    _fields_ = (
        ('header', Header),
        ('action', ctypes.c_int))
    _pack_ = 1


class AddNotifyCmd(ctypes.Structure):
    _fields_ = (
        ('header', Header),
        ('port', ctypes.c_ushort))
    _pack_ = 0


RmNotifyCmd = AddNotifyCmd

print("Header:%s" % (ctypes.sizeof(Header),))
print("SetActionCmd:%s" % (ctypes.sizeof(SetActionCmd), ))
print("AddNotifyCmd:%s" % (ctypes.sizeof(AddNotifyCmd), ))
# exit(1)
