from dataclasses import dataclass
from operator import itemgetter
from typing import Any, List, Tuple

from plcx.bag.pack import list_to_bytes
from plcx.constants import BYTE_ORDER
from plcx.utils.boolean import BIT_ORDER


@dataclass
class Writer:
    tag: Tuple[str, Any]  # (<format>, <value>)
    arguments: List[Tuple[str, str]]  # (<name>, <format>)
    byte_order: str = BYTE_ORDER
    bit_order: str = BIT_ORDER

    def write(self, **kwargs) -> bytes:
        """
        Write args or kwargs to bytes message.

        :param kwargs: arguments define as kwargs
        :return: bytes message
        """
        tag_format_, tag_value = self.tag
        format_ = tag_format_ + "".join([f for _, f in self.arguments])
        arguments_names = [name for name, _ in self.arguments if name]
        if arguments_names:
            args = itemgetter(*arguments_names)(kwargs)
            args = (args,) if not isinstance(args, tuple) else args  # convert args to tuple
        else:
            args = ()

        return list_to_bytes(
            format_=format_, args=(tag_value,) + args, byte_order=self.byte_order, bit_order=self.bit_order,
        )
