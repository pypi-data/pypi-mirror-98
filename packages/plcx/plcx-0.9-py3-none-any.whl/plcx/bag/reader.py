import logging
import struct
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from plcx.bag.unpack import bytes_to_dict
from plcx.constants import BYTE_ORDER
from plcx.utils.boolean import BIT_ORDER

logger = logging.getLogger(__name__)


@dataclass
class Reader:
    tag: Tuple[str, Any]  # (<format>, <value>)
    arguments: List[Tuple[Optional[str], str]]  # (<name>, <format>)
    byte_order: str = BYTE_ORDER
    bit_order: str = BIT_ORDER

    def _read(self, message: bytes) -> Dict[str, Any]:
        """
        Unpack message to dictionary.

        :param message: bytes message
        :return: dictionary with parameters
        """
        tag_format, _ = self.tag
        return bytes_to_dict(
            message, [("tag", tag_format)] + self.arguments, byte_order=self.byte_order, bit_order=self.bit_order,
        )

    def is_readable(self, message: bytes) -> bool:
        """
        Test if reader could read message.

        :param message: bytes message
        :return: bool value
        """
        _, exp_value = self.tag
        try:
            value = self._read(message).get("tag", None)
        except struct.error:
            logger.debug(f"Reader could not read message `{message}`.")
            return False
        else:
            logger.debug(f"Reader read tag value `{value}` and expected `{exp_value}`.")
            return value == exp_value

    def read(self, message: bytes) -> Dict[str, Any]:
        """
        Unpack message to dictionary.

        :param message: bytes message
        :return: dictionary with parameters
        """
        response = self._read(message)
        _ = response.pop("tag")  # remove tag from output
        return response
