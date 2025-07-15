from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.endpoints import router
from app.api.authentication import authenticate_user, create_access_token, get_current_user

app = FastAPI(title="Sample Management API", version="1.0.0")
app.include_router(router, prefix="/api", dependencies=[Depends(get_current_user)])

@app.post("/auth/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """
    Endpoint to authenticate a user and return an access token.
    :param form_data: The form data containing username and password.
    :return: A dictionary containing the access token and its type.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    else:
        access_token = create_access_token(data={"sub": user["username"]})
        return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user = Depends(get_current_user)) -> dict:
    """
    Endpoint to get the current authenticated user's information.
    :param current_user: The current user obtained from the authentication dependency.
    :return: A dictionary containing the current user's information.
    """
    return current_user
