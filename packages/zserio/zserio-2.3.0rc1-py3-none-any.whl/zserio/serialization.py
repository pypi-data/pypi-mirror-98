"""
The module provides help methods for serialization and deserialization of generated objects.
"""

import typing

from zserio.bitwriter import BitStreamWriter
from zserio.bitbuffer import BitBuffer
from zserio.bitreader import BitStreamReader

def serialize(obj: typing.Any) -> BitBuffer:
    """
    Serializes generated object to the bit buffer.

    Because serialization to the bit buffer does not have to be byte aligned (divisible by 8), it's possible
    that not all bits of the last byte are used. In this case, only most significant bits of the corresponded
    size are used.

    :param obj: Generated object to serialize.
    :returns: Bit buffer which represents generated object in binary format.
    :raises PythonRuntimeException: Throws in case of any error during serialization.
    """

    writer = BitStreamWriter()
    obj.write(writer)

    return BitBuffer(writer.byte_array, writer.bitposition)

def deserialize(obj_class: typing.Type[typing.Any], bitbuffer: BitBuffer, *args) -> typing.Any:
    """
    Deserializes bit buffer to the generated object.

    :param obj_class: Class instance of the generated object to deserialize.
    :param bitbuffer: Bit buffer which represents generated object in binary format.
    :param args: Additional arguments needed for obj_class.from_reader method.
    :returns: Generated object created from given bit buffer.
    :raises PythonRuntimeException: Throws in case of any error during deserialization.
    """

    reader = BitStreamReader.from_bitbuffer(bitbuffer)

    return obj_class.from_reader(reader, *args)

def serialize_to_bytes(obj: typing.Any) -> bytes:
    """
    Serializes generated object to the byte buffer.

    This is a convenient method for users which do not need exact number of bits to which the given object
    will be serialized.

    However, it's still possible that not all bits of the last byte are used. In this case, only most
    significant bits of the corresponding size are used.

    :param obj: Generated object to serialize.
    :returns: Bytes which represents generated object in binary format.
    :raises PythonRuntimeException: Throws in case of any error during serialization.
    """

    bitbuffer = serialize(obj)

    return bitbuffer.buffer

def deserialize_bytes(obj_class: typing.Type[typing.Any], buffer: bytes, *args) -> typing.Any:
    """
    Deserializes byte buffer to the generated object.

    This method can potentially use all bits of the last byte even if not all of them were written during
    serialization (because there is no way how to specify exact number of bits). Thus, it could allow reading
    behind stream (possibly in case of damaged data).

    :param obj_class: Class instance of the generated object to deserialize.
    :param buffer: Byte buffer which represents generated object in binary format.
    :param args: Additional arguments needed for obj_class.from_reader method.
    :returns: Generated object created from given byte buffer.
    :raises PythonRuntimeException: Throws in case of any error during deserialization.
    """

    bitbuffer = BitBuffer(buffer)

    return deserialize(obj_class, bitbuffer, *args)
