from fastapi import APIRouter, Depends

from schemas.account import AccountCreatePayload
from schemas.transaction import DepositTransactionPayload
from services.account import account_service
from deps import get_current_user


account_router = APIRouter()


@account_router.post("")
def create_account(
    account_data: AccountCreatePayload,
    current_user=Depends(get_current_user)
):
    new_account = account_service.create_account(account_data, current_user)
    return new_account


@account_router.get("")
def get_account(current_user=Depends(get_current_user)):
    account = account_service.get_account(current_user)
    return account


@account_router.post("/{account_id}/deposit")
def transact(account_id: str, transaction: DepositTransactionPayload, current_user=Depends(get_current_user)):
    return account_service.deposit_fund(transaction, account_id)

@account_router.post("/{account_id}/withdraw")
def withdraw(account_id: str, transaction: DepositTransactionPayload, current_user=Depends(get_current_user)):
    return account_service.withdraw_fund(transaction, account_id, current_user)
