from fastapi import APIRouter, Depends, HTTPException, Query
from database import get_session
from models import Order, OrderCreate, OrderUpdate, StatusLog, OrderStatus
from sqlmodel import Session, select
from datetime import datetime


router = APIRouter(prefix="/orders", tags=["orders"])   

@router.post("/", response_model=Order)
def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    db_order = Order(**order.model_dump()) #our model is a pydantic model, so we can use model_dump to convert it to a dict
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


@router.get("/", response_model=list[Order])
def list_orders(
    status: OrderStatus | None = Query(default=None, description="Filter by order status"),
    created_date: str | None = Query(default=None, description="Filter by creation date (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session)
):
    query = select(Order)

    if status:
        query = query.where(Order.status == status)

    if created_date:
        start = datetime.combine(created_date, datetime.min.time()) 
        #if we don't specify the time, it will default to 00:00:00, so we need to set the time to the minimum time of the day
        #why do we require datetime.comibine? Because created_date is a date object, 
        # and we need to convert it to a datetime object to compare it with the created_at field in the database,
        #  which is a datetime field. 
        end = datetime.combine(created_date, datetime.max.time())
        query = query.where(Order.created_at >= start, Order.created_at <= end)

    query = query.offset(skip).limit(limit)

    return session.exec(query).all()