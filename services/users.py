from models import User
from repositories.users import UserRepository
from schemas import UserCreate
from security import get_password_hash, verify_password
from exceptions import UsernameExisting, UserUnauthorized


class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def register(self, user_data: UserCreate) -> User:
        existing = await self._repository.find_by_username(user_data.username)
        if existing is not None:
            raise UsernameExisting
        user = User(username=user_data.username, hashed_password=get_password_hash(user_data.password))
        return await self._repository.save(user)

    async def authenticate(self, username: str, password: str) -> User:
        user = await self._repository.find_by_username(username)
        if user is None or not verify_password(password, user.hashed_password):
            raise UserUnauthorized
        return user

    async def get_user_by_username(self, username: str) -> User:
        return await self._repository.find_by_username(username)
