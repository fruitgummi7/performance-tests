from fastapi import FastAPI, APIRouter, status, HTTPException
from pydantic import BaseModel, EmailStr, RootModel

app = FastAPI()

users_router = APIRouter(
    prefix="/api/v1/users",
    tags=["users-service"]
)

class UserIn(BaseModel):
    email: EmailStr
    username: str


class UserOut(UserIn):
    id: int

class UsersStore(RootModel):
    root: list[UserOut]

    def find(self, user_id: int) -> UserOut | None:
        return next(filter(lambda user: user.id == user_id, self.root), None)

    def create(self, user_in: UserIn) -> UserOut:
        user = UserOut(id=len(self.root) + 1, **user_in.model_dump())
        self.root.append(user)
        return user

    def update(self, user_id: int, user_in: UserIn) -> UserOut:
        index = next(index for index, user in enumerate(self.root) if user.id == user_id)
        updated = UserOut(id=user_id, **user_in.model_dump())
        self.root[index] = updated
        return updated

    def delete(self, user_id: int) -> None:
        self.root = [user for user in self.root if user.id != user_id]

store = UsersStore(root=[])

@users_router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    if not (user := store.find(user_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user

@users_router.get("", response_model=list[UserOut])
async def get_users():
    return store.root

@users_router.post("", response_model=UserOut)
async def create_user(user: UserIn):
    return store.create(user)

@users_router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserIn):
    if not store.find(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return store.update(user_id, user)

@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    if not store.find(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return store.delete(user_id)

app.include_router(users_router)