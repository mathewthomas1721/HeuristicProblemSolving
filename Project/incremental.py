base_mult = 1.25
base_pen = 1.5

def toForm(num):
    if (num > 1000000):
        return num.toExponential(3)
    else:
        round_num = num.toFixed(0)
        if int(round_num) < num:
            return (num + 1).toFixed(0)
        else:
            return round_num

def toForm2(num):
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




class Game:
    def __init__(self, props, upgrades):
        self.counter = 0
        self.time = 0
        self.currency = 6.0
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
        self.time += 1
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
            self.counter = 0
            self.pen_count += 1

    def cycle(self):
        Game.cycle(self)
        if self.counter >= 20:
            self.pen_count += 1
            self.counter = 0
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
        ('Expanding Nim', 6.0, base_mult, 1.0),
        ('Stoplight Shortest Path', 50.0, base_mult, 6.0),
        ('No Tipping', 400.0, base_mult, 35.0),
        ('Gravitational Voronoi', 2000.0, base_mult, 144.0),
        ('Evasion',  10000.0, base_mult, 600.0),
        ('Dancing Without Stars',  50000.0, base_mult, 2200.0),
        ('Compatibility Game',  400000.0, base_mult, 11111.0),
        ('Auction Game',  2000000.0, base_mult, 40000.0)
    ]]

    upgrades = [list (tupl) for tupl in [
        ('Dynamic Programming', 0, 40, 2.0),
        ("Dijkstra's Algorithm", 1, 250, 2.0),
        ('Dynamic Programming', 2, 3000, 2.0),
        ('Clustering', 3, 18000, 2.0),
        ('No Diagonal Walls', 4, 80000, 2.0),
        ('Simulated Annealing', 5, 500000, 2.0),
        ('Depth First Search', 6, 7000000, 2.0),
        ('Be First Bidder', 7, 33000000, 2.0),
    ]]

    penalties = [list (tupl) for tupl in [
        ('Cost Increase 1', 0, 0, base_pen),
        ('Cost Increase 2', 0, 1, base_pen),
        ('Cost Increase 3', 0, 2, base_pen),
        ('Cost Increase 4', 0, 3, base_pen),
        ('Cost Increase 5', 0, 4, base_pen),
        ('Cost Increase 6', 0, 5, base_pen),
        ('Cost Increase 7', 0, 6, base_pen),
        ('Cost Increase 8', 0, 7, base_pen),
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
        document.getElementById("resDiv").innerHTML = "Game Over. Player earned ${} in {} seconds.".format(toForm2(self.gm.currency), self.endtime)
        window.clearInterval(self.inter)
        window.removeEventListener('keydown', self.respondKey)

    def BuyProp(self, n):
        self.gm.buy_prop(n - 1)
        prop = self.gm.properties[n-1]
        document.getElementById ('prop'+ str(n)) .innerHTML = "You've developed {} {} algorithms. Earning {} KitKats per second.".format (prop.count, prop.name, toForm2(prop.total_income))
        document.getElementById ('PC'+ str(n)) .innerHTML = 'Cost: {} KitKats'.format (toForm(prop.cost))
        document.getElementById('cash').innerHTML = 'Total KitKats: {}'.format(toForm2(self.gm.currency))
        document.getElementById('tt' + str(n)).innerHTML = "Each {} algorithm earns {} KitKats per second".format(prop.name, toForm2(prop.income))
        if self.two_player:
            document.getElementById ('advcount') .innerHTML = 'Adversary has {} penalties to apply'.format(self.gm.pen_count)



    def UpgradeProp(self, n):
        self.gm.upgrade_prop(n - 1)
        prop = self.gm.properties[n-1]
        document.getElementById('cash').innerHTML = 'Total KitKats: {}'.format(toForm2(self.gm.currency))
        document.getElementById ('prop'+ str(n)) .innerHTML = "You've developed {} {} algorithms. Earning {} KitKats per second.".format (prop.count, prop.name, toForm2(prop.total_income))
        document.getElementById('tt' + str(n)).innerHTML = "Each {} algorithm earns {} KitKats per second".format(prop.name, toForm2(prop.income))
        ug = prop.get_next_upgrade()
        document.getElementById('ttu' + str(n)).innerHTML = 'Purchase "{}" for ${}. Multipy all {} earnings by {}'.format(ug.name, toForm(ug.cost), prop.name, ug.mult)
        document.getElementById('ttu' + str(n)).innerHTML = 'Multipy all {} earnings by {}'.format(prop.name, ug.mult)
        document.getElementById('UC' + str(n)).innerHTML = 'Upgrade : {} KitKats'.format(toForm(ug.cost))

    def ApplyPenalty(self, n):
        self.gm.applyPenalty(n - 1)
        document.getElementById ('advcount') .innerHTML = 'Adversary has {} penalties to apply'.format(self.gm.pen_count)
        prop = self.gm.properties[n-1]
        document.getElementById ('PC'+ str(n)) .innerHTML = 'Cost: {} KitKats'.format (toForm(prop.cost))
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
        document.getElementById('cash').innerHTML = 'Total KitKats: {}'.format(toForm2(self.gm.currency))
        if self.two_player:
            document.getElementById ('advcount') .innerHTML = 'Adversary has {} penalties to apply'.format(self.gm.pen_count)
        if self.gm.time >= self.endtime:
            self.EndGame()



    def Setup(self):
        textbox = document.getElementById("timeSet")
        self.endtime = int(textbox.elements[0].value)
        if self.endtime == 0:
            self.endtime = 1000000000

        document.getElementById("startButtons").style.display = "none"
        document.getElementById("resDiv").style.display = "none"
        if self.two_player:
            document.getElementById("adPane").style.display = "inline-block"
        document.getElementById("cash").style.display = "inline-block"
        for n in [1,2,3,4,5,6,7,8]:
            document.getElementById("sec" + str(n)).style.display = "inline-block"
        self.inter = window.setInterval(self.Update, 1000)
        document.getElementById('cash').innerHTML = 'Total Cash: ${}'.format(toForm2(self.gm.currency))
        if self.two_player:
            document.getElementById ('advcount') .innerHTML = 'Adversary has {} penalties to apply'.format(self.gm.pen_count)
        if self.two_player:
            document.getElementById ('advcount') .innerHTML = 'Adversary has {} penalties to apply'.format(self.gm.pen_count)
        for n in [1,2,3,4,5,6,7,8]:
            prop = self.gm.properties[n-1]
            if self.two_player:
                document.getElementById ('tta'+str(n)) .innerHTML = 'Increase cost of {} by a factor of {}'.format(prop.name, self.gm.penalties[n-1].mult.toFixed(2))
            document.getElementById ('prop'+ str(n)) .innerHTML = "You've developed {} {} algorithms. Earning {} KitKats per second.".format (prop.count, prop.name, toForm2(prop.total_income))
            document.getElementById ('PC'+ str(n)) .innerHTML = 'Cost: {} KitKats'.format (toForm(prop.cost))
            document.getElementById('tt' + str(n)).innerHTML = "Each {} algorithm earns {} KitKats per second".format(prop.name, toForm2(prop.income))
            ug = prop.get_next_upgrade()
            document.getElementById('ttu' + str(n)).innerHTML = 'Multipy all {} earnings by {}'.format(prop.name, ug.mult)
            document.getElementById('UC' + str(n)).innerHTML = 'Upgrade : {} KitKats'.format(toForm(ug.cost))



game = incremental ()
