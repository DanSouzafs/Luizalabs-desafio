from fastapi import APIRouter, HTTPException, status

from src.exceptions import BusinessError
from src.schemas.auth import LoginIn
from src.services.auth import AuthService
from src.views.auth import LoginOut

router = APIRouter(prefix="/auth")

auth_service = AuthService()


@router.post("/login", response_model=LoginOut)
async def login(data: LoginIn):
    try:
        return await auth_service.authenticate_user(data.username, data.password)
    except BusinessError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
