from http.client import HTTPException

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED
from models.jwt_user import JWTUser
from routes.v1 import app_v1
from routes.v2 import app_v2
from utils.const import TOKEN_DESCRIPTION, TOKEN_SUMMARY
from utils.security import check_jwt_token, authenticate_user, create_jwt_token
from datetime import datetime

app = FastAPI(title="Bookstore API Documentation",
              description="It is an API that is used for bookstore.",
              version="1.0.0")
app.include_router(app_v1, prefix="/v1", dependencies=[Depends(check_jwt_token)])
app.include_router(app_v2, prefix="/v2", dependencies=[Depends(check_jwt_token)])


@app.post("/token", description=TOKEN_DESCRIPTION, summary=TOKEN_SUMMARY)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt_user_dict = {"username": form_data.username,
                     "password": form_data.password}
    jwt_user = JWTUser(**jwt_user_dict)
    user = authenticate_user(jwt_user)
    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    jwt_token = create_jwt_token(user)
    return {"access_token": jwt_token}


@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.now()

    # modify request
    if not any(word in str(request.url) for word in ["/token", "/docs", "/openapi.json"]):
        try:
            jwt_token = request.headers["Authorization"].split("Bearer ")[1]
            is_valid = check_jwt_token(jwt_token)
        except Exception as e:
            is_valid = False

        if not is_valid:
            return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)

    response = await call_next(request)
    # modify response
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["x-execution-time"] = str(execution_time)
    return response
