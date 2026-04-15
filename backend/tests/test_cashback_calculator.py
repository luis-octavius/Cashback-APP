from decimal import Decimal

from app.cashback_calculator import calculate_cashback


def test_vip_600_with_20_percent_discount() -> None:
    result = calculate_cashback("vip", Decimal("600"), Decimal("20"))

    assert result["final_amount"] == Decimal("480.00")
    assert result["cashback_amount"] == Decimal("26.40")


def test_regular_600_with_10_percent_discount() -> None:
    result = calculate_cashback("regular", Decimal("600"), Decimal("10"))

    assert result["final_amount"] == Decimal("540.00")
    assert result["cashback_amount"] == Decimal("54.00")


def test_vip_600_with_15_percent_discount() -> None:
    result = calculate_cashback("vip", Decimal("600"), Decimal("15"))

    assert result["final_amount"] == Decimal("510.00")
    assert result["cashback_amount"] == Decimal("53.55")


def test_threshold_applies_only_above_500() -> None:
    equal_result = calculate_cashback("regular", Decimal("500"), Decimal("0"))
    above_result = calculate_cashback("regular", Decimal("500.01"), Decimal("0"))

    assert equal_result["cashback_amount"] == Decimal("25.00")
    assert above_result["cashback_amount"] == Decimal("50.00")
