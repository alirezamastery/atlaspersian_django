from enum import Enum


__all__ = [
    'APIErrorCodes'
]


class APIErrorCodes(Enum):
    INVALID_MOBILE = 1
    MOBILE_ALREADY_EXISTS = 2
    MOBILE_NOT_REGISTERED = 3
    INVALID_OTP = 4
    OTP_EXPIRED = 5

    INVALID_VARIANT_QUANTITY = 6
    INVALID_DISCOUNT_CODE = 7

