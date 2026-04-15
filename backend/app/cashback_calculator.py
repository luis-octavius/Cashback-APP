from decimal import Decimal, ROUND_HALF_UP

BASE_RATE = Decimal("0.05")
VIP_BONUS_RATE = Decimal("0.10")
THRESHOLD_VALUE = Decimal("500.00")
THRESHOLD_MULTIPLIER = Decimal("2")
HUNDRED = Decimal("100")
TWOPLACES = Decimal("0.01")


def to_money(value: Decimal) -> Decimal:
    return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def calculate_cashback(customer_type: str, purchase_amount: Decimal, discount_percent: Decimal) -> dict:
    discount_rate = discount_percent / HUNDRED

    # calcula diretamente o valor restante após o desconto
    final_amount = purchase_amount * (Decimal("1") - discount_rate)

    # cálculo de cashback base
    base_cashback = final_amount * BASE_RATE

    # aplica o dobro do cashback caso a quantia final seja maior que 500
    threshold_multiplier_applied = final_amount > THRESHOLD_VALUE
    if threshold_multiplier_applied:
        base_cashback = base_cashback * THRESHOLD_MULTIPLIER

    # calcula o cashback adicional DEPOIS de calcular o base, caso o cliente seja vip
    vip_bonus = Decimal("0")
    if customer_type == "vip":
        vip_bonus = (final_amount * BASE_RATE) * VIP_BONUS_RATE

    cashback = base_cashback + vip_bonus

    return {
        "final_amount": to_money(final_amount),
        "base_cashback": to_money(final_amount * BASE_RATE),
        "vip_bonus": to_money(vip_bonus),
        "cashback_amount": to_money(cashback),
        "threshold_multiplier_applied": threshold_multiplier_applied,
    }
