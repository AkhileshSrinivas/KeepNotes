from fastapi import APIRouter, Depends
from services.verify import AuthUsers

# ----------------------
# Router for Home Page endpoints
# ----------------------
home_router = APIRouter(
    tags=["Home Page"]
)

# ----------------------
# Home Page Endpoint
# ----------------------
@home_router.post("/")
async def homePage(current_user: dict = Depends(AuthUsers.get_current_user)):
    """
    Home Page API endpoint.

    Returns a personalized greeting message for the currently logged-in user.

    Parameters:
    - current_user (dict): Automatically injected by FastAPI using JWT authentication.
      Contains user details such as 'id' and 'name'.

    Returns:
    - str: Greeting message with the user's name.
    """
    # Access the 'name' field from the authenticated user's data
    return f"Good Morning {current_user['name']}!"
