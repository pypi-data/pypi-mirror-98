class TutukaException(Exception):
    def __init__(self, message='', code=None):
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return '<{class_name} {code}: {message}>'.format(
            class_name=self.__class__.__name__,
            code=self.code,
            message=self.message,
        )


class DuplicateTransaction(TutukaException):
    """Duplicate Transaction ID."""


class InvalidCardID(TutukaException):
    """Invalid Card Identifier."""


class OperationNotAllowed(TutukaException):
    """Operation not Allowed."""


class OperationNotSupported(TutukaException):
    """Operation not Supported."""


class TransactionTimeout(TutukaException):
    """Transaction Timeout."""


class AuthenticationFailed(TutukaException):
    """Authentication Failed."""


class OperationDeclined(TutukaException):
    """Do not honor (general decline, no specific reason given)."""


class CardAlreadyActive(TutukaException):
    """Card already active."""


class CardNotActive(TutukaException):
    """Card not active."""


class ExpiredCard(TutukaException):
    """Expired card."""


class LostCard(TutukaException):
    """Lost card."""


class StolenCard(TutukaException):
    """Stolen card."""


class InvalidLastName(TutukaException):
    """Invalid last name."""


class InvalidFirstName(TutukaException):
    """Invalid first name."""


class InvalidID(TutukaException):
    """Invalid ID number."""


class InvalidMSISDN(TutukaException):
    """Invalid MSISDN."""


class ReferenceWithoutLinkedCard(TutukaException):
    """Reference has no linked cards."""


class ReferenceWithDuplicatedLinkedCard(TutukaException):
    """Card already linked to a different reference."""


class InsufficientFunds(TutukaException):
    """No enough funds for operation."""


class WithdrawalsLimitExceeded(TutukaException):
    """Exceeds number of withdrawals."""


class InvalidAmount(TutukaException):
    """Amount is not valid."""


class SecurityViolation(TutukaException):
    """Something went wrong during authorization."""


class IncorrectPin(TutukaException):
    """Not valid PIN."""


class PinTriesExceeded(TutukaException):
    """Exceeds number of pin tries."""


class InvalidPinBlock(TutukaException):
    """Invalid PIN block."""


class PinLengthError(TutukaException):
    """Length of PIN is not valid."""


class SuspectFraud(TutukaException):
    """Unusual operation detected."""


class MonthlyLoadAmountExceeded(TutukaException):
    """Exceeds allowed amount."""


class InvalidClient(TutukaException):
    """Invalid Client."""


class InvalidAccount(TutukaException):
    """Invalid Account."""


class BlockedAccount(TutukaException):
    """Account blocked."""
