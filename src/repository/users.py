from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User
from src.schemas import UserCreate

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.db = session
    
    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_user_name(self, user_name: str) -> User | None:
        stmt = select(User).where(User.user_name == user_name)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()
    
    async def get_user_by_user_email(self, user_email: str) -> User | None:
        stmt = select(User).where(User.user_email == user_email)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()
    
    async def create_user(self, body: UserCreate, avatar: str = None) -> User:
        user = User(
            **body.model_dump(exclude_unset=True, exclude={"password"}),
            hashed_password=body.password,
            avatar=avatar
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user