from fastapi import HTTPException, status
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate
from app.models.user import User

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_in: UserCreate) -> User:
        existing_user = await self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )
        
        # Note: A secure password hashing library such as passlib with bcrypt 
        # should be used here to process user_in.password before storage.
        hashed_password = "process_with_secure_hashing_library" 
        
        return await self.user_repo.create(user_in, hashed_password)
