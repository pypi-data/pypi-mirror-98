﻿# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from typing import Union
from .invalid_packet_exception_data import InvalidPacketExceptionData
from ..protobufs import main_pb2
from .motion_lib_exception import MotionLibException


class InvalidPacketException(MotionLibException):
    """
    Thrown when a packet from a device cannot be parsed.
    """

    @property
    def details(self) -> InvalidPacketExceptionData:
        """
        Additional data for InvalidPacketException
        """
        return self._details

    def __init__(self, message: str, custom_data: Union[bytes, InvalidPacketExceptionData]):
        MotionLibException.__init__(self, message)

        if isinstance(custom_data, InvalidPacketExceptionData):
            self._details = custom_data
        else:
            protobuf_obj = main_pb2.InvalidPacketExceptionData()
            protobuf_obj.ParseFromString(custom_data)
            self._details = InvalidPacketExceptionData.from_protobuf(protobuf_obj)
