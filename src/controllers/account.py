from fastapi import APIRouter, Depends, status

from src.schemas.account import AccountIn
from src.security import get_current_user, login_required
from src.services.account import AccountService
from src.services.transaction import TransactionService
from src.views.account import AccountOut, TransactionOut

router = APIRouter(prefix="/accounts", dependencies=[Depends(login_required)])

account_service = AccountService()
tx_service = TransactionService()


@router.get("/", response_model=list[AccountOut])
async def read_accounts(
    limit: int,
    skip: int = 0,
    current_user: dict = Depends(get_current_user),
):
    return await account_service.read_all(
        user_id=current_user["user_id"], limit=limit, skip=skip
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AccountOut)
async def create_account(
    account: AccountIn, current_user: dict = Depends(get_current_user)
):
    return await account_service.create(account, current_user["user_id"])


@router.get("/{id}/transactions", response_model=list[TransactionOut])
async def read_account_transactions(
    id: int,
    limit: int,
    skip: int = 0,
    current_user: dict = Depends(get_current_user),
):
    return await tx_service.read_all(
        account_id=id, user_id=current_user["user_id"], limit=limit, skip=skip
    )
