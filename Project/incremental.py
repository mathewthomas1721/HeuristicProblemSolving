
class Property:
    def __init__(self,name, base_cost, cost_mult, base_income):
        self.name = name
        self.cost = base_cost
        self.mult = cost_mult
        self.income = base_income
        self.count = 0.0
        self.total_income = 0.0;
        self.upgrades_Available = []

    def get_income(self):
        return self.income



    def inc_cost(self):
        self.cost *= self.mult

    def buy(self):
        self.count += 1
        self.total_income = self.count * self.income

    def get_next_upgrade(self):
        return self.upgrades_Available[0]

    def upgrade(self):
        ug = self.upgrades_Available[0]
        self.income *= ug.mult
        if len(self.upgrades_Available) == 1:
            ug.cost *= 10
        else:
            self.upgrades_Available.pop(0)
        self.total_income = self.count * self.income

class Upgrade:
    def __init__(self, name, cost, mult):
        self.name = name
        self.cost = cost
        self.mult = mult

class Penalty:
    def __init__(self,pen):
        self.name = pen[0]
        if pen[1] == 0:
            self.type = 0
            self.prop = pen[2]
            self.mult = pen[3]
        elif pen[1] == 1:
            self.type = 1
            self.mult = pen[2]
            self.duration = pen[3]
            self.time_left = self.duration
        else:
            self.name = "Florg"




class Game:
    def __init__(self, props, upgrades):
        self.counter = 0
        self.currency = 10.0
        self.pen_count = 0
        self.properties = []
        self.global_multiplier = 1.0
        for prop in props:
            self.properties.append(Property(prop[0], prop[1], prop[2], prop[3]))
        for ug in upgrades:
            self.properties[ug[1]].upgrades_Available.append(Upgrade(ug[0], ug[2], ug[3]))


    def buy_prop(self, prop_to_buy):
        prop = self.properties[prop_to_buy]
        if self.currency >= prop.cost:
            self.currency -= prop.cost
            prop.inc_cost()
            prop.buy()
            return True
        return False

    def upgrade_prop(self, prop_to_upgrade):
        prop = self.properties[prop_to_upgrade]
        ug = prop.upgrades_Available[0]
        if self.currency >= ug.cost:
            self.currency -= ug.cost
            prop.upgrade()
            return True
        return False

    def cycle(self):
        self.counter += 1
        for prop in self.properties:
            self.currency += prop.total_income * self.global_multiplier


class Two_Player_Game(Game):
    def __init__(self, props, upgrades, penalties):
        Game.__init__(self, props, upgrades)
        self.penalties = []
        self.active_penalties = []
        for pen in penalties:
            self.penalties.append(Penalty(pen))
        for prop in self.properties:
            prop.mult = 1.0

    def buy_prop(self, prop_to_buy):
        succeed = Game.buy_prop(self, prop_to_buy)
        if succeed:
            self.pen_count += 1

    def cycle(self):
        Game.cycle(self)
        if self.counter % 25 == 0:
            self.pen_count += 1
        new_active = self.active_penalties
        self.active_penalties = []
        for pen in self.active_penalties:
            pen.time_left -= 1
            if pen.time_left == 0:
                self.global_multiplier *= (1.0 / pen.mult)
                pen.time_left = pen.duration
            else:
                self.active_penalties.append(pen)


    def applyPenalty(self, pen_no):
        if self.pen_count > 0:
            self.pen_count -= 1
            pen = self.penalties[pen_no]
            pen.name = "florg1"
            if pen.type == 0:
                self.properties[pen.prop].cost *= pen.mult
            elif pen.type == 1:
                self.active_penalties.append(pen)
                self.global_multiplier *= pen.mult


class incremental:

    properties = [list (tupl) for tupl in [
        ('Burger Stand', 10.0, 1.15, 1.0),
        ('Diner', 100.0, 1.15, 8.0),
        ('Gas Station', 1000.0, 1.15, 60.0),
        ('Wal-Mart', 8000.0, 1.15, 420.0),
        ('Bank',  65000.0, 1.15, 2500.0),
        ('Department Store',  210000.0, 1.15, 9000.0),
        ('Auto Manufacturer',  4000000.0, 1.15, 100000.0),
        ('Conglomerate',  100000000.0, 1.15, 2000000.0)
    ]]

    upgrades = [list (tupl) for tupl in [
        ('Better Burgers', 0, 10, 2.0),
        ('Saltier Fries', 1, 10, 2.0),
        ('Premium Gas', 2, 10, 2.0),
        ('Cheaper Labor', 3, 10, 2.0),
        ('Subprime Mortgage', 4, 10, 2.0),
        ('New Advertising Campaign', 5, 10, 2.0),
        ('Cheat Safety Regulations', 6, 10, 2.0),
        ('Outsourcing', 7, 10, 2.0),
    ]]

    penalties = [list (tupl) for tupl in [
        ('Cost Increase 1', 0, 0, 1.15),
        ('Cost Increase 2', 0, 1, 1.15),
        ('Cost Increase 3', 0, 2, 1.15),
        ('Cost Increase 4', 0, 3, 1.15),
        ('Cost Increase 5', 0, 4, 1.15),
        ('Cost Increase 6', 0, 5, 1.15),
        ('Cost Increase 7', 0, 6, 1.15),
        ('Cost Increase 8', 0, 7, 1.15),
        ('Penalty 1', 1, 0.5, 100),

    ]]


    def __init__ (self, two_player):
        window.setInterval(self.Update, 1000)
        self.two_player = two_player
        if two_player:
            self.gm = Two_Player_Game(self.properties,self.upgrades, self.penalties)
        else:
            self.gm = Game(self.properties, self.upgrades)


    def BuyProp(self, n):
        self.gm.buy_prop(n - 1)
        prop = self.gm.properties[n-1]
        if (prop.cost > 1000000):
            pcost = prop.cost.toExponential(3)
        else:
            pcost = prop.cost.toFixed(0)
        document.getElementById ('prop'+ str(n)) .innerHTML = 'You own {} {}s. Cost for next: ${}'.format (prop.count, prop.name, pcost)
        if (self.gm.currency < 1000000):
            curr = self.gm.currency.toFixed(0)
        else:
            curr = self.gm.currency.toExponential(3)
        document.getElementById('cash').innerHTML = 'Total Cash: ${}'.format(curr)
        document.getElementById('tt' + str(n)).innerHTML = "Your {}s are producing ${} per second.".format(prop.name, prop.total_income)


    def UpgradeProp(self, n):
        self.gm.upgrade_prop(n - 1)
        if (self.gm.currency < 1000000):
            curr = self.gm.currency.toFixed(0)
        else:
            curr = self.gm.currency.toExponential(3)
        document.getElementById('cash').innerHTML = 'Total Cash: ${}'.format(curr)
        ug = prop.get_next_upgrade()
        document.getElementById('ttu' + str(n)).innerHTML = 'Purchase "{}" for ${}. Multipy all {} income by {}'.format(ug.name, ug.cost, prop.name, ug.mult)


    def ApplyPenalty(self, n):
        self.gm.applyPenalty(n - 1)
        document.getElementById ('adv1') .innerHTML = 'Adversary has {} penalties to apply. Next Penalty {}.'.format(self.gm.pen_count, self.gm.penalties[0].name)
        for n in [1,2,3,4,5,6,7,8]:
            prop = self.gm.properties[n-1]
            if (prop.cost > 1000000):
                pcost = prop.cost.toExponential(3)
            else:
                pcost = prop.cost.toFixed(0)
            document.getElementById ('prop'+ str(n)) .innerHTML = 'You own {} {}s. Cost for next: ${}'.format (prop.count, prop.name, pcost)


    def Update (self):
        self.gm.cycle()
        if (self.gm.currency < 1000000):
            curr = self.gm.currency.toFixed(0)
        else:
            curr = self.gm.currency.toExponential(3)
        document.getElementById('cash').innerHTML = 'Total Cash: ${}'.format(curr)
        if self.two_player:
            document.getElementById ('adv1') .innerHTML = 'Adversary has {} penalties to apply. Next Penalty {}.'.format(self.gm.pen_count, self.gm.penalties[0].name)
        for n in [1,2,3,4,5,6,7,8]:
            prop = self.gm.properties[n-1]
            if (prop.cost > 1000000):
                pcost = prop.cost.toExponential(3)
            else:
                pcost = prop.cost.toFixed(0)
            document.getElementById ('prop'+ str(n)) .innerHTML = 'You own {} {}s. Cost for next: ${}'.format (prop.count, prop.name, pcost)
            document.getElementById('tt' + str(n)).innerHTML = "Your {}s are producing ${} per second.".format(prop.name, prop.total_income)
            ug = prop.get_next_upgrade()
            document.getElementById('ttu' + str(n)).innerHTML = 'Purchase "{}" for ${}. Multipy all {} income by {}'.format(ug.name, ug.cost, prop.name, ug.mult)





game = incremental (True)