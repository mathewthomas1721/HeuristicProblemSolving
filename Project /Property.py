class Property:
    def __init__(self,name, base_cost, cost_mult, base_income):
        self.name = name
        self.cost = base_cost
        self.mult = cost_mult
        self.income = base_income
        self.count = 0.0
        self.total_income = 0.0;

    def get_income(self):
        return self.income

    def inc_cost(self):
        self.cost *= self.mult

    def buy(self):
        self.count += 1
        self.total_income = self.count * self.income

    def upgrade(self, multiplier):
        self.income *= multiplier



class Upgrade:
    def __init__(self, name, prop, cost, mult):
        self.name = name
        self.prop = prop
        self.cost = cost
        self.mult = mult
