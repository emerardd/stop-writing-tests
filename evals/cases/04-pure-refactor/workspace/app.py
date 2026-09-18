def total(items):
    value = 0
    for price, quantity in items:
        value += price * quantity
    return value
