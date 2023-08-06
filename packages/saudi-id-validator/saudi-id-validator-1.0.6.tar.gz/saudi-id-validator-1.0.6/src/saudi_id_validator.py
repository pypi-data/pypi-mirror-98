from typing import Union


def validate(id_number: Union[int, str]) -> bool:
    """Validate format and checksum of the identity number.

    :param id_number: Saudi Arabian identity number
    :type id_number: int or str
    """

    digits = [int(d) for d in str(id_number)]

    if len(digits) != 10 or digits[0] not in [1, 2]:
        return False

    odd_sum = sum(digits[-1::-2])
    even_sum = sum([sum(divmod(2 * d, 10)) for d in digits[-2::-2]])
    checksum = (odd_sum + even_sum) % 10

    return bool(checksum == 0)
