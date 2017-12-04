

def toForm(num):
    if (num > 1000000):
        return num.toExponential(3)
    else:
        return num.toFixed(0)

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
        ('Expanding Nim Problem', 10.0, 1.15, 1.0),
        ('Stoplight Shortest Path Problem', 100.0, 1.15, 8.0),
        ('No Tipping Problem', 1000.0, 1.15, 60.0),
        ('Gravitational Voronoi Problem', 8000.0, 1.15, 420.0),
        ('Evasion',  65000.0, 1.15, 2500.0),
        ('Dancing Without Stars Problem',  210000.0, 1.15, 9000.0),
        ('Compatibility Problem',  4000000.0, 1.15, 100000.0),
        ('Auction Problem',  100000000.0, 1.15, 2000000.0)
    ]]

    upgrades = [list (tupl) for tupl in [
        ('Develop Better Algorithm', 0, 10, 2.0),
        ('Develop Better Algorithm', 1, 10, 2.0),
        ('Develop Better Algorithms', 2, 10, 2.0),
        ('Develop Better Algorithm', 3, 10, 2.0),
        ('Develop Better Algorithm', 4, 10, 2.0),
        ('Develop Better Algorithm', 5, 10, 2.0),
        ('Develop Better Algorithm', 6, 10, 2.0),
        ('Develop Better Algorithm', 7, 10, 2.0),
    ]]

    penalties = [list (tupl) for tupl in [
        ('Cost Increase 1', 0, 0, 1.25),
        ('Cost Increase 2', 0, 1, 1.25),
        ('Cost Increase 3', 0, 2, 1.25),
        ('Cost Increase 4', 0, 3, 1.25),
        ('Cost Increase 5', 0, 4, 1.25),
        ('Cost Increase 6', 0, 5, 1.25),
        ('Cost Increase 7', 0, 6, 1.25),
        ('Cost Increase 8', 0, 7, 1.25),
        ('Penalty 1', 1, 0.5, 100),

    ]]


    def __init__ (self):
        self.endtime = 100000000




    def StartOnePlayer(self):

        self.gm = Game(self.properties, self.upgrades)
        self.two_player = False
        self.Setup()

    def StartTwoPlayer(self):

        self.gm = Two_Player_Game(self.properties,self.upgrades, self.penalties)
        window.addEventListener('keydown', self.respondKey)
        self.two_player = True
        self.Setup()

    def EndGame(self):
        document.getElementById("adPane").style.display = "none"
        document.getElementById("cash").style.display = "none"
        for n in [1,2,3,4,5,6,7,8]:
            document.getElementById("sec" + str(n)).style.display = "none"
        document.getElementById("startButtons").style.display = "inline-block"
        document.getElementById("resDiv").style.display = "inline-block"
        document.getElementById("resDiv").innerHTML = "Game Over. Player earned ${} in {} seconds.".format(toForm(self.gm.currency), self.endtime)
        window.clearInterval(self.inter)
        window.removeEventListener('keydown', self.respondKey)

    def BuyProp(self, n):
        self.gm.buy_prop(n - 1)
        prop = self.gm.properties[n-1]
        document.getElementById ('prop'+ str(n)) .innerHTML = 'You developed {} {} algorithms'.format (prop.count, prop.name)
        document.getElementById ('PC'+ str(n)) .innerHTML = 'Cost: {} KitKats'.format (toForm(prop.cost))
        document.getElementById('cash').innerHTML = 'Total KitKats: {}'.format(toForm(self.gm.currency))
        document.getElementById('tt' + str(n)).innerHTML = "Your {}s are earning {} KitKats per second".format(prop.name, toForm(prop.total_income))
        if self.two_player:
            document.getElementById ('advcount') .innerHTML = 'Adversary has {} penalties to apply'.format(self.gm.pen_count)



    def UpgradeProp(self, n):
        self.gm.upgrade_prop(n - 1)
        prop = self.gm.properties[n-1]
        document.getElementById('cash').innerHTML = 'Total KitKats: {}'.format(toForm(self.gm.currency))
        document.getElementById('tt' + str(n)).innerHTML = "Your {} algorithms are earning {} KitKats per second".format(prop.name, toForm(prop.total_income))
        ug = prop.get_next_upgrade()
        document.getElementById('ttu' + str(n)).innerHTML = 'Purchase "{}" for ${}. Multipy all {} earnings by {}'.format(ug.name, toForm(ug.cost), prop.name, ug.mult)
        document.getElementById('ttu' + str(n)).innerHTML = 'Multipy all {} earnings by {}'.format(prop.name, ug.mult)
        document.getElementById('UC' + str(n)).innerHTML = 'Upgrade : {} KitKats'.format(toForm(ug.cost))

    def ApplyPenalty(self, n):
        self.gm.applyPenalty(n - 1)
        document.getElementById ('advcount') .innerHTML = 'Adversary has {} penalties to apply'.format(self.gm.pen_count)
        for n in [1,2,3,4,5,6,7,8]:
            prop = self.gm.properties[n-1]
            document.getElementById ('prop'+ str(n)) .innerHTML = 'You developed {} {} algorithms Cost for next: {} KitKats'.format (prop.count, prop.name, toForm(prop.cost))
            document.getElementById ('tta'+str(n)) .innerHTML = 'Increase cost of {} by a factor of {}'.format(prop.name, self.gm.penalties[n].mult.toFixed(2))


    def respondKey(self, event):
        self.keyCode = event.keyCode
        if self.keyCode == ord ('1'):
            self.ApplyPenalty(1)
        elif self.keyCode == ord ('2'):
            self.ApplyPenalty(2)
        elif self.keyCode == ord ('3'):
            self.ApplyPenalty(3)
        elif self.keyCode == ord ('4'):
            self.ApplyPenalty(4)
        elif self.keyCode == ord ('5'):
            self.ApplyPenalty(5)
        elif self.keyCode == ord ('6'):
            self.ApplyPenalty(6)
        elif self.keyCode == ord ('7'):
            self.ApplyPenalty(7)
        elif self.keyCode == ord ('8'):
            self.ApplyPenalty(8)

    def Update (self):
        self.gm.cycle()
        document.getElementById('cash').innerHTML = 'Total KitKats: {}'.format(toForm(self.gm.currency))
        if self.two_player:
            document.getElementById ('advcount') .innerHTML = 'Adversary has {} penalties to apply'.format(self.gm.pen_count)
        if self.gm.counter >= self.endtime:
            self.EndGame()



    def Setup(self):
        textbox = document.getElementById("timeSet")
        self.endtime = int(textbox.elements[0].value)
        if self.endtime == 0:
            self.endtime = 1000000000

        document.getElementById("startButtons").style.display = "none"
        if self.two_player:
            document.getElementById("adPane").style.display = "inline-block"
        document.getElementById("resDiv").style.display = "none"
        document.getElementById("cash").style.display = "inline-block"
        for n in [1,2,3,4,5,6,7,8]:
            document.getElementById("sec" + str(n)).style.display = "inline-block"
        self.inter = window.setInterval(self.Update, 1000)
        document.getElementById('cash').innerHTML = 'Total Cash: ${}'.format(toForm(self.gm.currency))
        if self.two_player:
            document.getElementById ('advcount') .innerHTML = 'Adversary has {} penalties to apply'.format(self.gm.pen_count)
        if self.two_player:
            document.getElementById ('advcount') .innerHTML = 'Adversary has {} penalties to apply'.format(self.gm.pen_count)
        for n in [1,2,3,4,5,6,7,8]:
            prop = self.gm.properties[n-1]
            if self.two_player:
                document.getElementById ('tta'+str(n)) .innerHTML = 'Increase cost of {} by a factor of {}'.format(prop.name, self.gm.penalties[n].mult.toFixed(2))
            document.getElementById ('prop'+ str(n)) .innerHTML = 'You developed {} {} algorithms'.format (prop.count, prop.name)
            document.getElementById ('PC'+ str(n)) .innerHTML = 'Cost: {} KitKats'.format (toForm(prop.cost))
            document.getElementById('tt' + str(n)).innerHTML = "Your {}s are earning {} KitKats per second".format(prop.name, toForm(prop.total_income))
            ug = prop.get_next_upgrade()
            document.getElementById('ttu' + str(n)).innerHTML = 'Multipy all {} earnings by {}'.format(prop.name, ug.mult)
            document.getElementById('UC' + str(n)).innerHTML = 'Upgrade : {} KitKats'.format(toForm(ug.cost))



game = incremental ()
