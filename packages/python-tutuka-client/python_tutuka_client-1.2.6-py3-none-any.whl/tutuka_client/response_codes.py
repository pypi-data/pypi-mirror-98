from types import MappingProxyType

from tutuka_client import errors

SUCCESS_RESPONSE_CODES = MappingProxyType({
    'APPROVED_NO_ACTION': 0,
    'APPROVED': 1,
})

ERROR_RESPONSE_CODES_EXCEPTIONS = MappingProxyType({
    '-3': errors.DuplicateTransaction,
    '-4': errors.InvalidCardID,
    '-5': errors.OperationNotAllowed,
    '-6': errors.OperationNotSupported,
    '-7': errors.TransactionTimeout,
    '-8': errors.AuthenticationFailed,
    '-9': errors.OperationDeclined,
    '-17': errors.InsufficientFunds,
    '-18': errors.WithdrawalsLimitExceeded,
    '-19': errors.InvalidAmount,
    '-24': errors.SecurityViolation,
    '-25': errors.IncorrectPin,
    '-26': errors.PinTriesExceeded,
    '-27': errors.InvalidPinBlock,
    '-28': errors.PinLengthError,
    '-34': errors.CardAlreadyActive,
    '-35': errors.CardNotActive,
    '-36': errors.ExpiredCard,
    '-37': errors.SuspectFraud,
    '-38': errors.LostCard,
    '-39': errors.StolenCard,
    '-100': errors.MonthlyLoadAmountExceeded,
    '-101': errors.BlockedAccount,
    '-102': errors.InvalidClient,
    '-103': errors.InvalidAccount,
    '-244': errors.InvalidLastName,
    '-246': errors.InvalidFirstName,
    '-247': errors.InvalidID,
    '-248': errors.InvalidMSISDN,
    '-778': errors.ReferenceWithoutLinkedCard,
    '-779': errors.ReferenceWithDuplicatedLinkedCard,
})
