from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from server.database import get_db
from server.schemas.response import HealthResponse, UserRequest
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
                        detail="Invalid access token."
                    )

                # Attach the "user_id" to the scope for the API to access
                scope['user_id'] = user_id
                await self.app(scope, receive, send)
                return
            except HTTPException as e:
                raise e
            except Exception as e:
                print('yoyoyo')
                print(f'{str(e)}\n{traceback.format_exc()}')

                status_code = e.get(
                    'status_code', status.HTTP_500_INTERNAL_SERVER_ERROR)
                detail = e.get('detail', 'Error while validating access toekn')

                raise HTTPException(
                    status_code=status_code,
                    detail=detail
                )


app.add_middleware(AuthMiddleware)
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
    try:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        user_account = UserAccount()
        user_account.user_id = db_user.id
        db.add(user_account)
        db.commit()
        db.refresh(user_account)

        return {
            'user': db_user,
            'account': user_account
        }
    except Exception as e:
        print(f'{str(e)}\n{traceback.format_exc()}')

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while creating user."
        )


@app.get("/auth", status_code=status.HTTP_200_OK, tags=["Auth"])
async def authenticate(user: UserRequest, db: Session = Depends(get_db)):
    '''
    Authenticate user and generate access token
    '''
    try:
        db_user = db.query(User).filter(User.username == user.username).first()

        if db_user and db_user.password == user.password:
            access_token = generate_jwt({'user_id': db_user.id})

            return {"access_token": access_token}

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid username or password.")
    except Exception as e:
        print(f'{str(e)}\n{traceback.format_exc()}')

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while authenticating user."
        )


@app.get("/user/balance", status_code=status.HTTP_200_OK, tags=["User"])
async def get_account_balance(user_id: int, db: Session = Depends(get_db)):
    '''
    Get user account balance
    '''
    try:
        account = db.query(UserAccount).filter(
            UserAccount.user_id == user_id).first()

        if account:
            return {"balance": account.balance}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found."
            )
    except Exception as e:
        print(f'{str(e)}\n{traceback.format_exc()}')

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while getting user balance."
        )


@app.patch("/user/deposit", status_code=status.HTTP_200_OK, tags=["User"])
async def deposit(user_id: int, amount: float, db: Session = Depends(get_db)):
    '''
    Deposit amount in user account
    '''
    try:
        with db.begin() as transaction:
            account = db.query(UserAccount).filter(
                UserAccount.user_id == user_id).with_for_update().first()

            if not account:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Account not found"
                )

            account.balance += amount
            transaction.commit()

            return {'message': f"${amount} deposited successfully."}
    except Exception as e:
        transaction.rollback()
        print(f'{str(e)}\n{traceback.format_exc()}')

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while depositing amount in user account."
        )


@app.patch("/user/withdraw", status_code=status.HTTP_200_OK, tags=["User"])
async def withdraw(user_id: int, amount: float, db: Session = Depends(get_db)):
    '''
    Withdraw amount from user account
    '''
    try:
        with db.begin() as transaction:
            account = db.query(UserAccount).filter(
                UserAccount.user_id == user_id).with_for_update().first()

            if not account:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Account not found"
                )

            if account.balance < amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient balance"
                )

            account.balance -= amount
            transaction.commit()

            return {'message': f"${amount} withdrawn successfully."}
    except Exception as e:
        transaction.rollback()
        print(f'{str(e)}\n{traceback.format_exc()}')

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while withdrawing amount from user account."
        )


@app.patch("/user/transfer", status_code=status.HTTP_200_OK, tags=["User"])
async def transfer_amount(user_id: int, to_user: int, amount: float, db: Session = Depends(get_db)):
    '''
    Transfer amount to given user account
    '''
    try:
        with db.begin() as transaction:
            sender_account = (
                db.query(UserAccount)
                .filter(UserAccount.user_id == user_id)
                .with_for_update()
                .first()
            )
            receiver_account = (
                db.query(UserAccount)
                .filter(UserAccount.user_id == to_user)
                .with_for_update()
                .first()
            )

            if not sender_account or not receiver_account:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Account not found"
                )

            if sender_account.balance < amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient balance"
                )

            sender_account.balance -= amount
            receiver_account.balance += amount
            transaction.commit()

        return {'message': f"{amount} transfered successfully."}
    except Exception as e:
        transaction.rollback()
        print(f'{str(e)}\n{traceback.format_exc()}')

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while transfering amount to user account."
        )
