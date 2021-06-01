import random


class OperPriceQuery:
    """
    根据手术名称和等级随机产生手术费用
    """
    def __init__(self, operation_name, operation_level = 1, *args, **kwargs) -> None:
        self.oper_name = operation_name
        self.oper_level = int(operation_level)

        self.factor = random.random() * len(self.oper_name) * 10
        self.price_range = [10000, int(10000 * self.factor)]
        self.large_factor = pow(2, self.oper_level)

    def query(self):
        price = random.randint(*self.price_range)
        price += random.random() * self.factor
        price *= self.large_factor
        price = round(price, 2)
        return price
