from databases.interfaces import Record

from src.database import database
from src.exceptions import AccountNotFoundError, UnauthorizedError
from src.models.account import accounts
from src.schemas.account import AccountIn


class AccountService:
    async def read_all(self, user_id: int, limit: int, skip: int = 0) -> list[Record]:
        # Filtrar apenas contas do usuário autenticado
        query = (
            accounts.select()
            .where(accounts.c.user_id == user_id)
            .limit(limit)
            .offset(skip)
        )
        return await database.fetch_all(query)

    async def get_by_id(self, account_id: int, user_id: int) -> Record:
        """Busca conta e verifica se pertence ao usuário"""
        query = accounts.select().where(accounts.c.id == account_id)
        account = await database.fetch_one(query)

        if not account:
            raise AccountNotFoundError

        if account.user_id != user_id:
            raise UnauthorizedError("You don't have access to this account")

        return account

    async def create(self, account: AccountIn, user_id: int) -> Record:
        # Garantir que a conta seja criada para o usuário autenticado
        command = accounts.insert().values(
            user_id=user_id,  # Usar user_id do token, não do request
            balance=account.balance,
        )
        account_id = await database.execute(command)

        query = accounts.select().where(accounts.c.id == account_id)
        return await database.fetch_one(query)
