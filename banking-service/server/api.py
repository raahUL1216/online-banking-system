from fastapi import FastAPI, Request, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from server.database import get_db
from server.schemas.misc import AmountRequest, HealthResponse, TransferRequest, UserRequest
from server.models.user import User, UserAccount
from server.utils.auth import generate_jwt, decode_jwt, path_dict

import traceback

app = FastAPI(
    title='Banking Service',
    description='Basic banking operation APIs for user.',
)


class AuthMiddleware:
    '''
    Middleware class to authenticate user
    '''

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        path = scope["path"]

        if path in path_dict:
            # skip auth for these paths
            await self.app(scope, receive, send)
            return
        else:
            # validate access token
            try:
                headers = dict(scope["headers"])
                access_token = headers.get(
                    b"authorization", b"").decode("utf-8")

                access_token = access_token.replace("Bearer ", "")
                user_id = decode_jwt(access_token)

                if not user_id:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Invalid access token'
                    )

                scope['user_id'] = user_id
                await self.app(scope, receive, send)
                return
            except HTTPException as e:
                print(f'{str(e)}\n{traceback.format_exc()}')
                raise e
            except Exception as e:
                print(f'{str(e)}\n{traceback.format_exc()}')

                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail='Error while validating access token'
                )


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.add_middleware(AuthMiddleware)


@app.get("/", status_code=status.HTTP_200_OK, tags=["Health check"])
async def health() -> HealthResponse:
    '''
    Health check API - Check if service is up.
    '''
    return HealthResponse(status="Ok")


@app.post("/register", status_code=status.HTTP_201_CREATED, tags=["Auth"])
async def register(user: UserRequest, db: Session = Depends(get_db)):
    '''
    Register user and create user account
    '''
    user = user.model_dump()

    existing_user = db.query(User).filter(
        User.username == user.get('username', '')).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username already exists."
        )

    db_user = User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    user_account = UserAccount()
    user_account.user_id = db_user.id
    db.add(user_account)
    db.commit()
    db.refresh(user_account)

    return {
        'id': db_user.id,
        'username': db_user.username,
        'account':  {
            'balance': user_account.balance,
            'last_updated': user_account.updated_at
        }
    }


@app.post("/auth", status_code=status.HTTP_200_OK, tags=["Auth"])
async def authenticate(user: UserRequest, db: Session = Depends(get_db)):
    '''
    Authenticate user and generate access token
    '''
    db_user = db.query(User).filter(User.username == user.username).first()

    if db_user and db_user.password == user.password:
        access_token = generate_jwt({'user_id': db_user.id})

        return {"access_token": access_token}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid username or password.'
    )


@app.get("/user/balance/", status_code=status.HTTP_200_OK, tags=["User"])
async def get_account_balance(request: Request, db: Session = Depends(get_db)):
    '''
    Get user account balance
    '''
    user_id = request.scope.get('user_id')
    account = db.query(UserAccount).filter(
        UserAccount.user_id == user_id).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found."
        )

    return {"balance": account.balance}


@app.patch("/user/deposit", status_code=status.HTTP_200_OK, tags=["User"])
async def deposit(request: Request, amount: AmountRequest, db: Session = Depends(get_db)):
    '''
    Deposit amount in user account
    '''
    try:
        user_id = request.scope.get('user_id')
        deposit_value = int(amount.value) or 0

        with db.begin() as transaction:
            account = db.query(UserAccount).filter(
                UserAccount.user_id == user_id).with_for_update().first()

            if not account:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Account not found"
                )

            account.balance += deposit_value

            return {'message': f"{deposit_value}₹ deposited successfully."}
    except Exception as error:
        print(f'{str(error)}\n{traceback.format_exc()}')
        raise error


@app.patch("/user/withdraw", status_code=status.HTTP_200_OK, tags=["User"])
async def withdraw(request: Request, amount: AmountRequest, db: Session = Depends(get_db)):
    '''
    Withdraw amount from user account
    '''
    try:
        user_id = request.scope.get('user_id')
        withdraw_value = int(amount.value) or 0

        with db.begin() as transaction:
            account = db.query(UserAccount).filter(
                UserAccount.user_id == user_id).with_for_update().first()

            if not account:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Account not found"
                )

            if account.balance < withdraw_value:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient balance"
                )

            account.balance -= withdraw_value

            return {'message': f"{withdraw_value}₹ withdrawn successfully."}
    except Exception as error:
        print(f'{str(error)}\n{traceback.format_exc()}')
        raise error


@app.patch("/user/transfer", status_code=status.HTTP_200_OK, tags=["User"])
async def transfer_amount(request: Request, transfer_to: TransferRequest, db: Session = Depends(get_db)):
    '''
    Transfer amount to given user account
    '''
    try:
        sender_user_id = request.scope.get('user_id')
        receiver_user_id = int(transfer_to.user_id) or 0
        transfer_amount = int(transfer_to.amount) or 0

        with db.begin() as transaction:
            sender_account = (
                db.query(UserAccount)
                .filter(UserAccount.user_id == sender_user_id)
                .with_for_update()
                .first()
            )
            receiver_account = (
                db.query(UserAccount)
                .filter(UserAccount.user_id == receiver_user_id)
                .with_for_update()
                .first()
            )

            if not sender_account or not receiver_account:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Account not found'
                )

            if sender_account.balance < transfer_amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient balance"
                )

            sender_account.balance -= transfer_amount
            receiver_account.balance += transfer_amount
            transaction.commit()

        return {'message': f"{transfer_amount}₹ transferred successfully."}
    except Exception as error:
        print(f'{str(error)}\n{traceback.format_exc()}')
        raise error
