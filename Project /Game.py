from Property import Property
from time import time

class Game:
    def __init__(self):
        self.currency = 10.0
        self.properties = []
        self.properties.append(Property("Burger Stand", 10.0, 1.15, 1))
        self.properties.append(Property("Diner", 100.0, 1.15, 12))
        self.upgrades_Available = []

    def buy_prop(self, prop):
        if self.currency >= prop.cost:
            self.currency -= prop.cost
            prop.inc_cost()
            prop.buy()
            return True
        return False

    def cycle(self):
        for prop in self.properties:
            self.currency += prop.total_income

    def run(self, purchase_file):
        pf = open(purchase_file, 'r')
        purchases = []
        for line in pf:
            purchases.append(int(line))
        ind = 0
        starttime = time()
        while True:
            clock = time()
            print int(self.currency)
            if ind < len(purchases):
                prop = self.properties[purchases[ind] - 1]
                if self.buy_prop(prop):
                    print "purchased Property " + prop.name
                    ind += 1
            self.cycle()
            while time() - clock < 0.1:
                pass


g = Game()
g.run("purchases.txt")
