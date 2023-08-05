﻿# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from typing import List
from ..protobufs import main_pb2


class StreamMovementInterruptedExceptionData:
    """
    Contains additional data for StreamMovementInterruptedException.
    """

    @property
    def warnings(self) -> List[str]:
        """
        The full list of warnings.
        """

        return self._warnings

    @warnings.setter
    def warnings(self, value: List[str]) -> None:
        self._warnings = value

    @property
    def reason(self) -> str:
        """
        The reason for the Exception.
        """

        return self._reason

    @reason.setter
    def reason(self, value: str) -> None:
        self._reason = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def from_protobuf(
        pb_data: main_pb2.StreamMovementInterruptedExceptionData
    ) -> 'StreamMovementInterruptedExceptionData':
        instance = StreamMovementInterruptedExceptionData.__new__(
            StreamMovementInterruptedExceptionData
        )  # type: StreamMovementInterruptedExceptionData
        instance.warnings = list(pb_data.warnings)
        instance.reason = pb_data.reason
        return instance
