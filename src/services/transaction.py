from decimal import Decimal
from databases.interfaces import Record

from src.database import database
from src.exceptions import AccountNotFoundError, BusinessError, UnauthorizedError
from src.models.account import accounts
from src.models.transaction import TransactionType, transactions
from src.schemas.transaction import TransactionIn


class TransactionService:
    async def read_all(
        self, account_id: int, user_id: int, limit: int, skip: int = 0
    ) -> list[Record]:
        # Verificar se a conta pertence ao usuário
        query = accounts.select().where(accounts.c.id == account_id)
        account = await database.fetch_one(query)

        if not account:
            raise AccountNotFoundError

        if account.user_id != user_id:
            raise UnauthorizedError("You don't have access to this account")

        # Buscar transações
        query = (
            transactions.select()
            .where(transactions.c.account_id == account_id)
            .limit(limit)
            .offset(skip)
        )
        return await database.fetch_all(query)

    @database.transaction()
    async def create(self, transaction: TransactionIn, user_id: int) -> Record:
        query = accounts.select().where(accounts.c.id == transaction.account_id)
        account = await database.fetch_one(query)

        if not account:
            raise AccountNotFoundError

        # Verificar se a conta pertence ao usuário
        if account.user_id != user_id:
            raise UnauthorizedError("You don't have access to this account")

        # Usar Decimal para cálculos monetários
        current_balance = Decimal(str(account.balance))
        amount = Decimal(str(transaction.amount))

        if transaction.type == TransactionType.WITHDRAWAL:
            balance = current_balance - amount
            if balance < 0:
                raise BusinessError("Operation not carried out due to lack of balance")
        else:
            balance = current_balance + amount

        # Create transaction entry
        transaction_id = await self.__register_transaction(transaction)
        # Update account balance
        await self.__update_account_balance(transaction.account_id, float(balance))

        query = transactions.select().where(transactions.c.id == transaction_id)
        return await database.fetch_one(query)

    async def __update_account_balance(self, account_id: int, balance: float) -> None:
        command = accounts.update().where(accounts.c.id == account_id).values(balance=balance)
        await database.execute(command)

    async def __register_transaction(self, transaction: TransactionIn) -> int:
        command = transactions.insert().values(
            account_id=transaction.account_id,
            type=transaction.type,
            amount=transaction.amount,
        )
        return await database.execute(command)
