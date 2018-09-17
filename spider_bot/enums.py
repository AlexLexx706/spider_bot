import ctypes

CMD_GET_STATE = 0
CMD_SET_ACTION = 1
CMD_ADD_NOTIFY = 2
CMD_RM_NOTIFY = 3
CMD_RM_NOTIFY = 4
CMD_SET_LEG_GEOMETRY = 5

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


class LegGeometry(ctypes.Structure):
    _fields_ = (
        ('pos', ctypes.c_float * 3),
        ('shoulder_offset', ctypes.c_float),
        ('shoulder_lenght', ctypes.c_float),
        ('forearm_lenght', ctypes.c_float),)
    _pack_ = 1


class LegDesc(ctypes.Structure):
    _fields_ = (
        ('geometry', LegGeometry),
        ('a_0', ctypes.c_float),
        ('a_1', ctypes.c_float),
        ('a_2', ctypes.c_float),)
    _pack_ = 1


class GetStateRes(ctypes.Structure):
    _fields_ = (
        ('header', ResHeader),
        ('body_mat', ctypes.c_float * 16),
        ('front_right_leg', LegDesc),
        ('front_left_leg', LegDesc),
        ('rear_right_leg', LegDesc),
        ('rear_left_leg', LegDesc))
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
    _pack_ = 1


RmNotifyCmd = AddNotifyCmd


class ManageServoCmd(ctypes.Structure):
    _fields_ = (
        ('header', Header),
        ('cmd', ctypes.c_uint8),
        ('address', ctypes.c_uint8),
        ('limmit', ctypes.c_float),)
    _pack_ = 1

    # commands enums
    NoneCmd = 0
    ResetAddressesCmd = 1
    SetAddressCmd = 2
    ResetLimmits = 3
    SetMinLimmitCmd = 4
    SetMaxLimmitCmd = 5
    LoadServosCmd = 6
    UnloadServosCmd = 7
    EnableSteringCmd = 8
    DisableSteringCmd = 9
    EnableReadAngles = 10
    DisableReadAngles = 11
    MoveServo = 12
    MoveServoSin = 13


class SetLegGeometry(ctypes.Structure):
    _fields_ = (
        ('header', Header),
        ('cmd', ctypes.c_uint32),
        ('geometry', LegGeometry),)
    _pack_ = 1


print("Header:%s" % (ctypes.sizeof(Header),))
print("SetActionCmd:%s" % (ctypes.sizeof(SetActionCmd), ))
print("AddNotifyCmd:%s" % (ctypes.sizeof(AddNotifyCmd), ))
# exit(1)
