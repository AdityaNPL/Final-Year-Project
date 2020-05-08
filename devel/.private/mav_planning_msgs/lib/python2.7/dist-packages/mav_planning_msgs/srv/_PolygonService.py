# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from mav_planning_msgs/PolygonServiceRequest.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct

import mav_planning_msgs.msg
import std_msgs.msg

class PolygonServiceRequest(genpy.Message):
  _md5sum = "b72bf7542ebf0f998ff6de9ed6f90873"
  _type = "mav_planning_msgs/PolygonServiceRequest"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """

mav_planning_msgs/PolygonWithHolesStamped polygon

================================================================================
MSG: mav_planning_msgs/PolygonWithHolesStamped
# A message to define a 2D polygon with holes, stamp, and altitude above ground.
Header header
float64 altitude
mav_planning_msgs/PolygonWithHoles polygon

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id

================================================================================
MSG: mav_planning_msgs/PolygonWithHoles
# A message to define a 2D polygon with holes.
mav_planning_msgs/Polygon2D hull
mav_planning_msgs/Polygon2D[] holes

================================================================================
MSG: mav_planning_msgs/Polygon2D
# A specification of a 2D polygon where the first and last points are assumed to be connected.
mav_planning_msgs/Point2D[] points

================================================================================
MSG: mav_planning_msgs/Point2D
# This contains the position of a 2D point.
float64 x
float64 y
"""
  __slots__ = ['polygon']
  _slot_types = ['mav_planning_msgs/PolygonWithHolesStamped']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       polygon

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(PolygonServiceRequest, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.polygon is None:
        self.polygon = mav_planning_msgs.msg.PolygonWithHolesStamped()
    else:
      self.polygon = mav_planning_msgs.msg.PolygonWithHolesStamped()

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      _x = self
      buff.write(_get_struct_3I().pack(_x.polygon.header.seq, _x.polygon.header.stamp.secs, _x.polygon.header.stamp.nsecs))
      _x = self.polygon.header.frame_id
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      buff.write(_get_struct_d().pack(self.polygon.altitude))
      length = len(self.polygon.polygon.hull.points)
      buff.write(_struct_I.pack(length))
      for val1 in self.polygon.polygon.hull.points:
        _x = val1
        buff.write(_get_struct_2d().pack(_x.x, _x.y))
      length = len(self.polygon.polygon.holes)
      buff.write(_struct_I.pack(length))
      for val1 in self.polygon.polygon.holes:
        length = len(val1.points)
        buff.write(_struct_I.pack(length))
        for val2 in val1.points:
          _x = val2
          buff.write(_get_struct_2d().pack(_x.x, _x.y))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    try:
      if self.polygon is None:
        self.polygon = mav_planning_msgs.msg.PolygonWithHolesStamped()
      end = 0
      _x = self
      start = end
      end += 12
      (_x.polygon.header.seq, _x.polygon.header.stamp.secs, _x.polygon.header.stamp.nsecs,) = _get_struct_3I().unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.polygon.header.frame_id = str[start:end].decode('utf-8')
      else:
        self.polygon.header.frame_id = str[start:end]
      start = end
      end += 8
      (self.polygon.altitude,) = _get_struct_d().unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      self.polygon.polygon.hull.points = []
      for i in range(0, length):
        val1 = mav_planning_msgs.msg.Point2D()
        _x = val1
        start = end
        end += 16
        (_x.x, _x.y,) = _get_struct_2d().unpack(str[start:end])
        self.polygon.polygon.hull.points.append(val1)
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      self.polygon.polygon.holes = []
      for i in range(0, length):
        val1 = mav_planning_msgs.msg.Polygon2D()
        start = end
        end += 4
        (length,) = _struct_I.unpack(str[start:end])
        val1.points = []
        for i in range(0, length):
          val2 = mav_planning_msgs.msg.Point2D()
          _x = val2
          start = end
          end += 16
          (_x.x, _x.y,) = _get_struct_2d().unpack(str[start:end])
          val1.points.append(val2)
        self.polygon.polygon.holes.append(val1)
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      _x = self
      buff.write(_get_struct_3I().pack(_x.polygon.header.seq, _x.polygon.header.stamp.secs, _x.polygon.header.stamp.nsecs))
      _x = self.polygon.header.frame_id
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      buff.write(_get_struct_d().pack(self.polygon.altitude))
      length = len(self.polygon.polygon.hull.points)
      buff.write(_struct_I.pack(length))
      for val1 in self.polygon.polygon.hull.points:
        _x = val1
        buff.write(_get_struct_2d().pack(_x.x, _x.y))
      length = len(self.polygon.polygon.holes)
      buff.write(_struct_I.pack(length))
      for val1 in self.polygon.polygon.holes:
        length = len(val1.points)
        buff.write(_struct_I.pack(length))
        for val2 in val1.points:
          _x = val2
          buff.write(_get_struct_2d().pack(_x.x, _x.y))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    try:
      if self.polygon is None:
        self.polygon = mav_planning_msgs.msg.PolygonWithHolesStamped()
      end = 0
      _x = self
      start = end
      end += 12
      (_x.polygon.header.seq, _x.polygon.header.stamp.secs, _x.polygon.header.stamp.nsecs,) = _get_struct_3I().unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.polygon.header.frame_id = str[start:end].decode('utf-8')
      else:
        self.polygon.header.frame_id = str[start:end]
      start = end
      end += 8
      (self.polygon.altitude,) = _get_struct_d().unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      self.polygon.polygon.hull.points = []
      for i in range(0, length):
        val1 = mav_planning_msgs.msg.Point2D()
        _x = val1
        start = end
        end += 16
        (_x.x, _x.y,) = _get_struct_2d().unpack(str[start:end])
        self.polygon.polygon.hull.points.append(val1)
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      self.polygon.polygon.holes = []
      for i in range(0, length):
        val1 = mav_planning_msgs.msg.Polygon2D()
        start = end
        end += 4
        (length,) = _struct_I.unpack(str[start:end])
        val1.points = []
        for i in range(0, length):
          val2 = mav_planning_msgs.msg.Point2D()
          _x = val2
          start = end
          end += 16
          (_x.x, _x.y,) = _get_struct_2d().unpack(str[start:end])
          val1.points.append(val2)
        self.polygon.polygon.holes.append(val1)
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill

_struct_I = genpy.struct_I
def _get_struct_I():
    global _struct_I
    return _struct_I
_struct_2d = None
def _get_struct_2d():
    global _struct_2d
    if _struct_2d is None:
        _struct_2d = struct.Struct("<2d")
    return _struct_2d
_struct_3I = None
def _get_struct_3I():
    global _struct_3I
    if _struct_3I is None:
        _struct_3I = struct.Struct("<3I")
    return _struct_3I
_struct_d = None
def _get_struct_d():
    global _struct_d
    if _struct_d is None:
        _struct_d = struct.Struct("<d")
    return _struct_d
# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from mav_planning_msgs/PolygonServiceResponse.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct


class PolygonServiceResponse(genpy.Message):
  _md5sum = "358e233cde0c8a8bcfea4ce193f8fc15"
  _type = "mav_planning_msgs/PolygonServiceResponse"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """
bool success

"""
  __slots__ = ['success']
  _slot_types = ['bool']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       success

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(PolygonServiceResponse, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.success is None:
        self.success = False
    else:
      self.success = False

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      buff.write(_get_struct_B().pack(self.success))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    try:
      end = 0
      start = end
      end += 1
      (self.success,) = _get_struct_B().unpack(str[start:end])
      self.success = bool(self.success)
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      buff.write(_get_struct_B().pack(self.success))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    try:
      end = 0
      start = end
      end += 1
      (self.success,) = _get_struct_B().unpack(str[start:end])
      self.success = bool(self.success)
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill

_struct_I = genpy.struct_I
def _get_struct_I():
    global _struct_I
    return _struct_I
_struct_B = None
def _get_struct_B():
    global _struct_B
    if _struct_B is None:
        _struct_B = struct.Struct("<B")
    return _struct_B
class PolygonService(object):
  _type          = 'mav_planning_msgs/PolygonService'
  _md5sum = '7e5305932db903eed4a95dd3377ac6bc'
  _request_class  = PolygonServiceRequest
  _response_class = PolygonServiceResponse