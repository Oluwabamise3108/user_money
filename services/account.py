from datetime import datetime
from decimal import Decimal
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from schemas.account import AccountCreatePayload, AccountCreate, Account
from database import accounts_collection
from database import transactions_collection
from schemas.transaction import DepositTransactionPayload
from schemas.transaction import WithdrawTransaction
from schemas.user import User
from serializers import account_serializer
from bson.objectid import ObjectId


class AccountService:

    @staticmethod
    def create_account(account_data: AccountCreatePayload, user: User) -> Account:
        account_data = account_data.model_dump()
        account_with_defaults = Account(
            **account_data,
            user_id=user.id,
            balance=0.0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        account_id = accounts_collection.insert_one(jsonable_encoder(account_with_defaults)).inserted_id
        account = accounts_collection.find_one({"_id": account_id})
        return account_serializer(account)

    @staticmethod
    def get_account(user: User):
        account = accounts_collection.find_one({"user_id": user.id})
        return account_serializer(account)

    @staticmethod
    def get_account_by_id(account_id: str):
        account = accounts_collection.find_one({"_id": ObjectId(account_id)})
        return account_serializer(account)

    @staticmethod
    def deposit_fund(deposit_payload: DepositTransactionPayload, account_id):
        account = AccountService.get_account_by_id(account_id)
        old_balance = float(account.balance)
        new_balance = old_balance + float(deposit_payload.amount)
        account.balance = new_balance
        account = accounts_collection.find_one_and_update(
            {"_id": ObjectId(account.id)},
            {"$set": {"balance": new_balance}}
        )
        return "successful"

    @staticmethod
    def withdraw_fund(transaction: DepositTransactionPayload, account_id: str, user: User):
        account = accounts_collection.find_one({"_id": ObjectId(account_id)})

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        if account.get("user_id") != user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to withdraw from this account")

        current_balance = float(account.get("balance", 0.0))
        amount_to_withdraw = float(transaction.amount)

        if amount_to_withdraw > current_balance:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        new_balance = current_balance - amount_to_withdraw

        accounts_collection.find_one_and_update(
            {"_id": ObjectId(account_id)},
            {"$set": {"balance": new_balance}}
        )

        transaction = WithdrawTransaction(
        account_id=account.id,
        amount=amount,
        )
        
        
        return {"message": "Withdrawal successful", "new_balance": new_balance}
    
account_service = AccountService()
