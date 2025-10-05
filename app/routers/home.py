from fastapi import APIRouter, Depends
from services.verify import AuthUsers

home_router = APIRouter(
    tags=["Home Page"]
)
@home_router.post("/")
async def homePage(current_user: dict = Depends(AuthUsers.get_current_user)):
    return f"Good Morning {current_user["name"]}!"