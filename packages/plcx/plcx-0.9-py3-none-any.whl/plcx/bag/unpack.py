import struct
from typing import Dict, List, Optional, Tuple, Union

from plcx.constants import BYTE_ORDER
from plcx.utils.boolean import BIT_ORDER, BOOLEAN_FORMAT_SYMBOL, byte_to_booleans
from plcx.utils.find import args_counts, remove_number

VALUE = Union[str, int, float, bool, List[bool]]


def bytes_to_list(msg: bytes, format_: str, byte_order: str = BYTE_ORDER, bit_order: str = BIT_ORDER) -> List[VALUE]:
    """
    Unpack bytes with define format to list.

    :param msg: bytes message
    :param format_: message format
    :param byte_order: indicate the byte order
    :param bit_order: bit order in one byte, `LSB` or `MSB` [LSB]
    :return: tuple with unpacked values
    """
    if not isinstance(msg, bytes):
        raise TypeError("Got unexpected type of message.")

    # count character in format
    arguments_count = args_counts(format_)

    # unpack bytes to tuple
    plcx_format = format_.replace(BOOLEAN_FORMAT_SYMBOL, "s")
    arguments = list(struct.unpack(f"{byte_order}{plcx_format}", msg))

    # group arguments and convert to boolean list
    bytes_list = []
    for c, count in arguments_count:
        if c == BOOLEAN_FORMAT_SYMBOL:
            boolean_list = byte_to_booleans(arguments.pop(0), bit_order=bit_order)
            bytes_list.append(boolean_list[0] if len(boolean_list) == 1 else boolean_list)
        elif count == 1 or c in ["c", "s"]:
            bytes_list.append(arguments.pop(0))
        else:
            bytes_list.append([arguments.pop(0) for _ in range(count)])

    return bytes_list


def bytes_to_dict(
    msg: bytes, config: List[Tuple[Optional[str], str]], byte_order: str = BYTE_ORDER, bit_order: str = BIT_ORDER,
) -> Dict[str, VALUE]:
    """
    Unpack bytes with define format to dictionary.

    :param msg: bytes message
    :param config: list of message components define as tuple, (<name>, <format>)
    :param byte_order: indicate the byte order
    :param bit_order: bit order in one byte, `LSB` or `MSB` [LSB]
    :return: dictionary with parameters name as keys and values as values
    """
    keys = [name for name, format_ in config if "x" != remove_number(format_)]
    values = bytes_to_list(
        msg=msg, format_="".join([f for _, f in config]), byte_order=byte_order, bit_order=bit_order,
    )
    return dict(zip(keys, values))
