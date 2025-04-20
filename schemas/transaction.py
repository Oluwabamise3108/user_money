from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from enum import Enum


class TransactionType(Enum):
    debit = "debit"
    credit = "credit"


class TransactionBase(BaseModel):
    transaction_type: TransactionType
    amount: Decimal


class DepositTransactionPayload(BaseModel):
    amount: Decimal


class DepositTransaction(BaseModel):
    account_id: str
    amount: Decimal
    transaction_type: str = TransactionType.credit.value
    date: datetime = datetime.now()


class WithdrawTransaction(BaseModel):
    account_id: str
    amount: Decimal
    transaction_type: str = TransactionType.debit.value
    date: datetime = datetime.now()


class TransactionDb(TransactionBase):
    account_id: str
    date: datetime
