from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from server.database import get_db

from server.models.statement import MonthlyStatement
from server.utils.statement import generate_monthly_statement
from server.schemas.misc import HealthResponse

import datetime


app = FastAPI(
    title='Statement Generation Service',
    description='Generates monthly transaction statement for user',
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


@app.get("/", status_code=status.HTTP_200_OK, tags=["Health check"])
async def health() -> HealthResponse:
    '''
    Health check API - Check if service is up.
    '''
    return HealthResponse(status="Ok")


@app.post("/statement/{user_id}/{month}/{year}", status_code=status.HTTP_201_CREATED, tags=["Auth"])
async def register(user_id: int, month: int, year: int, db: Session = Depends(get_db)):
    '''
    Generate and save monthly statement for user
    '''
    user_id = int(user_id) or 0
    month = int(month) or 0
    year = int(year) or 0
    current_year = datetime.date.today().year

    is_month_valid = (1 <= month <= 12)
    is_year_valid = (year and year <= current_year)

    if not user_id or not is_month_valid or not is_year_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request. Pass valid user_id or month or year."
        )

    # generate monthly statement and save it to db
    statement = generate_monthly_statement(user_id, month, year)

    monthly_statement = MonthlyStatement(**statement)
    db.add(monthly_statement)
    db.commit()
