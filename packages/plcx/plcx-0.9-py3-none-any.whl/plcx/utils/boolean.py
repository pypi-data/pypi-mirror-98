from typing import List, NoReturn, Tuple, Union

BOOLEAN_FORMAT_SYMBOL = "#"
BOOL_VALUE = Union[int, bool]
VALID_BIT_ORDERS = ["MSB", "LSB"]
BIT_ORDER = "MSB"


def validate_bit_order(bit_order) -> NoReturn:
    """Validate bit order parameter."""
    if bit_order not in VALID_BIT_ORDERS:
        raise AttributeError(f"except `LSB` or `MSB` bit order, got `{bit_order}`")


def byte_to_booleans(bytes_: bytes, bit_order: str = BIT_ORDER) -> List[List[bool]]:
    """
    Convert byte to list of booleans.

    :param bytes_: bytes convert to lists
    :param bit_order: bit order in one byte, `LSB` or `MSB` [LSB]
    :return: tuple with list of boolean
    """
    validate_bit_order(bit_order)
    order_range = range(7, -1, -1) if bit_order == BIT_ORDER else range(8)
    # unpacked byte to bits
    return [[bool(1 << i & byte) for i in order_range] for byte in bytes_]


def boolean_to_byte(
    booleans: Union[List[List[BOOL_VALUE]], Tuple[List[BOOL_VALUE]], List[BOOL_VALUE]], bit_order: str = BIT_ORDER,
) -> bytes:
    """
    Convert list of bool or int (0 or 1) values to bytes. Length of list must be at least 8.

    :param booleans: list of bool or int value
    :param bit_order: bit order in one byte, `LSB` or `MSB` [LSB]
    :return: one byte
    """
    validate_bit_order(bit_order)

    result = bytes()  # create empty result
    booleans = booleans if isinstance(booleans[0], (list, tuple)) else [booleans]  # convert to list of booleans
    # iter throw list og booleans
    for boolean_list in booleans:
        if len(boolean_list) > 8:
            raise TypeError("function to_byte expected list with max len of 8")

        boolean_list = list(boolean_list) + [0] * (8 - len(boolean_list))  # convert to 8 bit if it's not
        boolean_list = boolean_list[::-1] if bit_order == BIT_ORDER else boolean_list  # apply bit order
        result += sum(b << i for i, b in enumerate(boolean_list)).to_bytes(1, "little")

    return result
