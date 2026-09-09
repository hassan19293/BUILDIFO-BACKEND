import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.customers import Customer
from app.schemas.customers import CustomerCreate, CustomerRead, CustomerUpdate


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
	return {"status": "ok", "service": "buildifo-api"}


@router.get("/customers", response_model=list[CustomerRead], tags=["customers"])
def list_customers(
	skip: int = Query(default=0, ge=0),
	limit: int = Query(default=50, ge=1, le=100),
	db: Session = Depends(get_db),
) -> list[Customer]:
	return list(db.scalars(select(Customer).order_by(Customer.id).offset(skip).limit(limit)))


@router.post(
	"/customers",
	response_model=CustomerRead,
	status_code=status.HTTP_201_CREATED,
	tags=["customers"],
)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)) -> Customer:
	customer = Customer(**payload.model_dump())
	db.add(customer)
	try:
		db.commit()
	except IntegrityError:
		db.rollback()
		raise HTTPException(status_code=409, detail="A customer with this email already exists")
	except SQLAlchemyError as exc:
		db.rollback()
		logger.exception("Failed to create customer")
		raise HTTPException(
			status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
			detail="Customer service is temporarily unavailable",
		) from exc
	db.refresh(customer)
	return customer


@router.get("/customers/{customer_id}", response_model=CustomerRead, tags=["customers"])
def get_customer(customer_id: int, db: Session = Depends(get_db)) -> Customer:
	customer = db.get(Customer, customer_id)
	if customer is None:
		raise HTTPException(status_code=404, detail="Customer not found")
	return customer


@router.patch("/customers/{customer_id}", response_model=CustomerRead, tags=["customers"])
def update_customer(
	customer_id: int,
	payload: CustomerUpdate,
	db: Session = Depends(get_db),
) -> Customer:
	customer = db.get(Customer, customer_id)
	if customer is None:
		raise HTTPException(status_code=404, detail="Customer not found")
	for field, value in payload.model_dump(exclude_unset=True).items():
		setattr(customer, field, value)
	try:
		db.commit()
	except IntegrityError:
		db.rollback()
		raise HTTPException(status_code=409, detail="A customer with this email already exists")
	db.refresh(customer)
	return customer


@router.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["customers"])
def delete_customer(customer_id: int, db: Session = Depends(get_db)) -> None:
	customer = db.get(Customer, customer_id)
	if customer is None:
		raise HTTPException(status_code=404, detail="Customer not found")
	db.delete(customer)
	db.commit()
