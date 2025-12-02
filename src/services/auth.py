import bcrypt
from databases.interfaces import Record

from src.database import database
from src.exceptions import BusinessError
from src.models.user import users
from src.security import sign_jwt


class AuthService:
    async def authenticate_user(self, username: str, password: str) -> dict:
        # Buscar usuário pelo username
        query = users.select().where(users.c.username == username)
        user = await database.fetch_one(query)

        if not user:
            raise BusinessError("Invalid username or password")

        # Verificar senha
        if not self._verify_password(password, user.hashed_password):
            raise BusinessError("Invalid username or password")

        # Gerar token JWT
        return sign_jwt(user_id=user.id)

    def _hash_password(self, password: str) -> str:
        """Gera hash da senha usando bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica se a senha está correta"""
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

