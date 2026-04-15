from decimal import Decimal

from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..cashback_calculator import calculate_cashback
from ..database import get_db
from ..ip_utils import extract_client_ip
from ..models import CashbackQuery
from ..schemas import CashbackRequest, CashbackResponse, HistoryItem, HistoryResponse


router = APIRouter(prefix="/api/v1/cashback", tags=["cashback"])


@router.post("/calculate", response_model=CashbackResponse)
def calculate_and_store(payload: CashbackRequest, request: Request, db: Session = Depends(get_db)) -> CashbackResponse:
    result = calculate_cashback(
        customer_type=payload.customer_type,
        purchase_amount=payload.purchase_amount,
        discount_percent=payload.discount_percent,
    )

    ip_address = extract_client_ip(request)
    history_row = CashbackQuery(
        ip_address=ip_address,
        customer_type=payload.customer_type,
        purchase_amount=Decimal(payload.purchase_amount),
        discount_percent=Decimal(payload.discount_percent),
        final_amount=result["final_amount"],
        cashback_amount=result["cashback_amount"],
    )

    db.add(history_row)
    db.commit()

    return CashbackResponse(
        customer_type=payload.customer_type,
        purchase_amount=payload.purchase_amount,
        discount_percent=payload.discount_percent,
        final_amount=result["final_amount"],
        cashback_amount=result["cashback_amount"],
        breakdown={
            "final_amount": result["final_amount"],
            "base_cashback": result["base_cashback"],
            "vip_bonus": result["vip_bonus"],
            "threshold_multiplier_applied": result["threshold_multiplier_applied"],
        },
    )


@router.get("/history", response_model=HistoryResponse)
def get_history(request: Request, db: Session = Depends(get_db)) -> HistoryResponse:
    ip_address = extract_client_ip(request)

    rows = db.scalars(
        select(CashbackQuery)
        .where(CashbackQuery.ip_address == ip_address)
        .order_by(CashbackQuery.created_at.desc())
    ).all()

    return HistoryResponse(
        ip_address=ip_address,
        items=[
            HistoryItem(
                id=row.id,
                customer_type=row.customer_type,
                purchase_amount=row.purchase_amount,
                discount_percent=row.discount_percent,
                final_amount=row.final_amount,
                cashback_amount=row.cashback_amount,
                created_at=row.created_at,
            )
            for row in rows
        ],
    )
