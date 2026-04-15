from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


CustomerType = Literal["regular", "vip"]


class CashbackRequest(BaseModel):
    customer_type: CustomerType
    purchase_amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    discount_percent: Decimal = Field(ge=0, le=100, max_digits=5, decimal_places=2)


class CashbackBreakdown(BaseModel):
    final_amount: Decimal
    base_cashback: Decimal
    vip_bonus: Decimal
    threshold_multiplier_applied: bool


class CashbackResponse(BaseModel):
    customer_type: CustomerType
    purchase_amount: Decimal
    discount_percent: Decimal
    final_amount: Decimal
    cashback_amount: Decimal
    breakdown: CashbackBreakdown


class HistoryItem(BaseModel):
    id: int
    customer_type: CustomerType
    purchase_amount: Decimal
    discount_percent: Decimal
    final_amount: Decimal
    cashback_amount: Decimal
    created_at: datetime


class HistoryResponse(BaseModel):
    ip_address: str
    items: list[HistoryItem]
