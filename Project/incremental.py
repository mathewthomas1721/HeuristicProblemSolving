
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

    def upgrade(self):
        ug = self.upgrades_Available.pop(0)
        self.income *= ug.mult
        self.total_income = self.count * self.income

class Upgrade:
    def __init__(self, name, cost, mult):
        self.name = name
        self.cost = cost
        self.mult = mult

class Player:
    def __init__(self, props, upgrades):
        self.currency = 10.0
        self.properties = []
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
        for prop in self.properties:
            self.currency += prop.total_income

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
        ('Upgrade 1', 0, 10, 2.0),
        ('Upgrade 1', 1, 10, 2.0),
        ('Upgrade 1', 2, 10, 2.0),
        ('Upgrade 1', 3, 10, 2.0),
        ('Upgrade 1', 4, 10, 2.0),
        ('Upgrade 1', 5, 10, 2.0),
        ('Upgrade 1', 6, 10, 2.0),
        ('Upgrade 1', 7, 10, 2.0),
        ('Upgrade 1', 0, 10, 2.0),
        ('Upgrade 1', 1, 10, 2.0),
        ('Upgrade 1', 2, 10, 2.0),
        ('Upgrade 1', 3, 10, 2.0),
        ('Upgrade 1', 4, 10, 2.0),
        ('Upgrade 1', 5, 10, 2.0),
        ('Upgrade 1', 6, 10, 2.0),
        ('Upgrade 1', 7, 10, 2.0),
        ('Upgrade 1', 0, 10, 2.0),
        ('Upgrade 1', 1, 10, 2.0),       
    ]]
        
        
    def __init__ (self):
        window.setInterval(self.Update, 500)
        self.player = Player(self.properties, self.upgrades)
        
        
    def BuyProp(self, n):
        self.player.buy_prop(n - 1)
        prop = self.player.properties[n-1]
        document.getElementById ('prop'+ str(n)) .innerHTML = 'You own {} {}s. Cost for next: {}'.format (prop.count, prop.name, int(prop.cost))
        document.getElementById('cash').innerHTML = 'Total Cash: {}'.format(int(self.player.currency))
            

    def UpgradeProp(self, n):
        self.player.upgrade_prop(n - 1)
        document.getElementById('cash').innerHTML = 'Total Cash: {}'.format(int(self.player.currency))


    def Update (self):
        self.player.cycle()
        document.getElementById('cash').innerHTML = 'Total Cash: {}'.format(int(self.player.currency))
        for n in [1,2,3,4,5,6,7,8]:
            prop = self.player.properties[n-1]
            document.getElementById ('prop'+ str(n)) .innerHTML = 'You own {} {}s. Cost for next: {}'.format (prop.count, prop.name, int(prop.cost))





            
game = incremental ()
    