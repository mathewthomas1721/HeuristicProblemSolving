#2017 Paul Fisher, Mathew Thomas : The Baby Snakes

#This is the standard cost increase multiplier for a single player game. Increase/decrease this to make game harder/easier
base_mult = 1.25

#This is the standard cost increase multiplier for a two player game. Increase/decrease this to tilt the balance of the game towards the adversary/player
base_pen = 1.5

#Put currency amounts in desired format. Amounts and costs are stored as floating point numbers, but we want to
#   display them as integers. For costs, we always round up, so that the property is always able to be purchased when
#   it appears that the player has enough currency. For values larger than 1,000,000, we display in scientific notation
#Params:
#   num : floating point number to put in proper format
# return: number in proper format (a String)
def toForm(num):
    if (num > 1000000): # cutoff for displaying in exponential form
        return num.toExponential(3) #Represent as exponential with 3 decimal placed
    else:
        round_num = num.toFixed(0)
        if int(round_num) < num:   #If toFixed has rounded down, add 1
            return (num + 1).toFixed(0)
        else:
            return round_num

#Put currency amounts in desired format. Amounts and costs are stored as floating point numbers, but we want to
#   display them as integers.  This function uses standard rounding. For values larger than 1,000,000, we display in scientific notation.
#Params:
#   num : floating point number to put in proper format
# return: number in proper format (a String)
def toForm2(num):
    if (num > 1000000):
        return num.toExponential(3)
    else:
        return num.toFixed(0)


#Return a singular or plural 'KitKat', depending on the amount
#Params:
#   n : amount of KitKats
def currencyName(n):
    if n == 1: # if the amount is 1, return the singular form
        return 'KitKat'
    else: #otherwise return the plural
        return 'KitKats'

#Class storing information for a property in the incremental game. In our case, a particular game or problem
class Property:
    #Create a new Property
    #Params:
    #   name : name of the property (e.g. "Burger Stand")
    #   base_cost : original cost to buy an instance of this property
    #   cost_mult : The factor by which the cost increases on each purchase in single player
    #   base_income : income of one of these properties, before any upgrades
    def __init__(self,name, base_cost, cost_mult, base_income):
        self.name = name
        self.cost = base_cost
        self.mult = cost_mult
        self.income = base_income
        self.count = 0.0    #number of this property owned
        self.total_income = 0.0;  #total income earned by all copies of this property
        self.upgrades_Available = []

    #return income per seond of one intstance of the property
    def get_income(self):
        return self.income


    #increase the cost of this property by its cost multiplier
    def inc_cost(self):
        self.cost *= self.mult

    #Increase the number of this property owned.
    def buy(self):
        self.count += 1
        self.total_income = self.count * self.income #total income is updated. count * income.

    #return the nexr available upgrade to this property
    def get_next_upgrade(self):
        return self.upgrades_Available[0]

    #Apply next upgrade to this property
    def upgrade(self):
        ug = self.upgrades_Available[0]
        self.income *= ug.mult #Upgrding will multiply the income by some factor
        if len(self.upgrades_Available) == 1: #If this is the last upgrade in the series, we keep it and increase its cost by a factor of 10
            ug.cost *= 10
        else:
            self.upgrades_Available.pop(0) # Otherwise we remove this upgrade as it could only be used once
        self.total_income = self.count * self.income

#Class containing information for an upgrade
class Upgrade:
    #Create a new upgrade
    #Params:
    #   name : name of this upgrade (this isn't visible to the user in this version)
    #   cost : base cost to purchase this upgrade
    #   mult : factor by which to multiply production of its property
    def __init__(self, name, cost, mult):
        self.name = name
        self.cost = cost
        self.mult = mult

#Class containing information for a penalty
class Penalty:
    #Create a new Penalty
    #Params:
    #   pen : a tuple containing name and other information for the penalty.
    #       in this game it is of the form (name, type, prop, mult)
    #       name : name of the penalty, string. Not visible in current version
    #       type : We implemented other types of penalties, but only the cost-increase made it into the final game, an int
    #       prop : The property being penalize, an int
    #       mult : the multiplier by which to increase cost of the property
    def __init__(self,pen):
        self.name = pen[0]
        if pen[1] == 0: #this allows the addition of other types of penalties in the future
            self.type = 0
            self.prop = pen[2]
            self.mult = pen[3]



#Class for an instance of a game. This class is instantiated in a single player game
class Game:
    #Setup game data
    #Params:
    #   props: A list of tuples containing info for the properties to be available in this game
    #           (name, base_cost, cost_mult, base_income) as specified above
    #   upgrades: A list of tuples containing info for the upgrades to be available
    #           (name, prop, cost, mult)
    #           prop : index of property being upgraded. Other fields are as defined above
    def __init__(self, props, upgrades):
        self.counter = 0 #counter for adversary's time-based earning of penalties
        self.time = 0   #time elapse in game in seconds
        self.currency = 6.0 #Initial currency for the player
        self.cum_currency = 0.0 #Gross currency earned by the player in this game
        self.pen_count = 0 #Number of penalties available to the adversary (if two player game)
        self.properties = []
        self.global_multiplier = 1.0 # not used in this version. Kept for possible use in new upgrades/penalties
        for prop in props:  #Add a property to this game for each tuple in the props list
            self.properties.append(Property(prop[0], prop[1], prop[2], prop[3]))
        for ug in upgrades: #Create each upgrade and add it to the appropriate property's list of upgrades
            self.properties[ug[1]].upgrades_Available.append(Upgrade(ug[0], ug[2], ug[3]))

    #Buy a property if the player has sufficient funds
    #Params:
    #   prop_to_buy : index of property the player wants to buy
    #return : True on success, False on failure
    def buy_prop(self, prop_to_buy):
        prop = self.properties[prop_to_buy]
        if self.currency >= prop.cost: # Only buy if the player has enough currency to pay the cost
            self.currency -= prop.cost
            prop.inc_cost()            #property cost increases on buy
            prop.buy()                 #Actually increment the number of the property owned
            return True
        return False


    #Upgrade a property with the next available upgrade
    #Params:
    #   prop_to_upgrade : index of property being upgrades
    #return : True on success, False on failure
    def upgrade_prop(self, prop_to_upgrade):
        prop = self.properties[prop_to_upgrade] # get property object
        ug = prop.upgrades_Available[0] #get upgrade from property's list
        if self.currency >= ug.cost: #Check if player can afford
            self.currency -= ug.cost
            prop.upgrade()
            return True
        return False

    #One game cycle. Called every second.
    def cycle(self):
        self.counter += 1 #one timestep
        self.time += 1
        for prop in self.properties: #Player receives income from all properties
            self.currency += prop.total_income * self.global_multiplier
            self.cum_currency += prop.total_income * self.global_multiplier

#Class for an instance of a two player game. Inherits from Game
class Two_Player_Game(Game):
    #Start a new two player game
    #Params:
    #   props: A list of tuples containing info for the properties to be available in this game
    #           (name, base_cost, cost_mult, base_income) as specified above
    #   upgrades: A list of tuples containing info for the upgrades to be available
    #           (name, prop, cost, mult)
    #           prop : index of property being upgraded. Other fields are as defined above
    #   penalties : A list of tuples containung info for penalties available to the adversary. Format as above
    def __init__(self, props, upgrades, penalties):
        Game.__init__(self, props, upgrades) #Call superclass constructor
        self.penalties = []
        self.active_penalties = []
        for pen in penalties: #Create each penalty object and add to list
            self.penalties.append(Penalty(pen))
        #Because in a two player game, the costs only increase through penalties
        for prop in self.properties:
            prop.mult = 1.0     #change all the property's cost_increas multipliers from their default value to 1.0


    #Buy a property if the player has sufficient funds
    #Params:
    #   prop_to_buy : index of property the player wants to buy
    def buy_prop(self, prop_to_buy):
        succeed = Game.buy_prop(self, prop_to_buy) #Superclass buy
        if succeed: #If the purchase goes through,
            self.counter = 0.  #Reset counter for next penalty
            self.pen_count += 1.    #and increment the number of penalties the adversary has.

    #One game cycle. Called every second.
    def cycle(self):
        Game.cycle(self)
        if self.counter >= 20: #If player has gone 20 seconds without a purchase,
            self.pen_count += 1 #give the adversary another penalty
            self.counter = 0
        #This is code for penalties that had a duration. Not used in final version.
        #new_active = self.active_penalties
        #self.active_penalties = []
        #for pen in new_active:
        #    pen.time_left -= 1
        #    if pen.time_left == 0:
        #        self.global_multiplier *= (1.0 / pen.mult)
        #        pen.time_left = pen.duration
        #    else:
        #        self.active_penalties.append(pen)

    #Apply a penalty to a property
    #Params:
    #   pen_no : The index of the penalty to apply
    def applyPenalty(self, pen_no):
        if self.pen_count > 0:  #only apply penlaty if the adversary has one available
            self.pen_count -= 1
            pen = self.penalties[pen_no] #get penalty object
            if pen.type == 0:
                self.properties[pen.prop].cost *= pen.mult #apply cost increase multiplier
            #used for penalties witha duration that affected global multiplier. Not used in final version
            #elif pen.type == 1: #used for
            #    self.active_penalties.append(pen)
            #    self.global_multiplier *= pen.mult


#Top level Class for running gamde and interacting with HTML
class incremental:
    #List of tuples for constructing the properties
    #Format: (name, base_cost, cost_mult, base_income)
    #Change names to change the theme of the game
    #Base costs and incomes can be tweaked to change the balance and progression of the game.
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

    #List of tuples for constructing the upgrades
    #Format : (name, property, base cost, multiplier)
    #The names are not currently used
    #base costs and multipliers can be tweaked to change the balance and progression of the game
    upgrades = [list (tupl) for tupl in [
        ('Dynamic Programming', 0, 40, 2.0),
        ("Dijkstra's Algorithm", 1, 250, 2.0),
        ('Dynamic Programming', 2, 3000, 2.0),
        ('Clustering', 3, 18000, 2.0),
        ('No Diagonal Walls', 4, 80000, 2.0),
        ('Simulated Annealing', 5, 500000, 2.0),
        ('Depth First Search', 6, 7000000, 2.0),
        ('Block Opponents', 7, 33000000, 2.0),
    ]]

    #List of tuples for constructing the penalties
    #Format: (name, type, property, cost_mult)
    #Names not currently used
    #All penalties in this game are type 0: cost multipliers
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

    #Default ending time for "infinite" game
    def __init__ (self):
        self.endtime = 100000000



    #Initialize a one player game. Function called on click of Single Player Game Button
    def StartOnePlayer(self):

        self.gm = Game(self.properties, self.upgrades) #set game to a new one playter game
        self.two_player = False
        self.Setup()

    #Initialize a two player game. Function called on click of Two Player Game Button
    def StartTwoPlayer(self):

        self.gm = Two_Player_Game(self.properties,self.upgrades, self.penalties) #set game to a new two playter game

        #Add event listener to map 1 - 8 keys to the penalty buttons
        window.addEventListener('keydown', self.respondKey)
        #These sections are only needed in a two player game, so make these visible here
        document.getElementById("ins").style.display = "inline-block"
        document.getElementById("adPane").style.display = "inline-block"

        self.two_player = True
        self.Setup()


    #End a game after time has expired
    def EndGame(self):

        #Make game playing sections invisible
        document.getElementById("adPane").style.display = "none"
        document.getElementById("cash").style.display = "none"
        document.getElementById("ins").style.display = "none"
        for n in [1,2,3,4,5,6,7,8]:
            document.getElementById("sec" + str(n)).style.display = "none"

        #Make the home screen buttons and result text visible
        document.getElementById("startButtons").style.display = "inline-block"
        document.getElementById("resDiv").style.display = "inline-block"

        #Set results text
        document.getElementById("resDiv").innerHTML = "Game Over. Player earned {} KitKats in {} seconds.".format(toForm2(self.gm.cum_currency), self.endtime)

        #Remove update function and key listener
        window.clearInterval(self.inter)
        window.removeEventListener('keydown', self.respondKey)

    #Called on property buy button press. Attempt to buy a property.
    #Params:
    #   n : 1-based index of property to buy
    def BuyProp(self, n):

        self.gm.buy_prop(n - 1)  #Attempt to buy the property
        prop = self.gm.properties[n-1]  #get property object

        #Update property text with new count and cost of property
        document.getElementById ('prop'+ str(n)) .innerHTML = "You've developed {} {} algorithms. <br>Earning {} {} per second.".format (prop.count, prop.name, toForm2(prop.total_income), currencyName(prop.total_income))
        document.getElementById ('PC'+ str(n)) .innerHTML = 'Cost: {} KitKats'.format (toForm(prop.cost))

        #Since player may have spent currency, update text that tracks current currency
        if (self.endtime - self.gm.time < 10000): #only display timer if there are less than 10000 seconds Remaining
            document.getElementById('cash').innerHTML = 'Total KitKats: {}<br>Remaining Time : {}'.format(toForm2(self.gm.currency), self.endtime - self.gm.time)
        else:
            document.getElementById('cash').innerHTML = 'Total KitKats: {}'.format(toForm2(self.gm.currency))

        #A sucessful purchase adds a penalty in two player, so update that text
        if self.two_player:
            document.getElementById ('advcount') .innerHTML = 'Available Penalties : {}'.format(self.gm.pen_count)


    #Called on property upgrade button press. Attempt to upgrade a property.
    #Params:
    #   n : 1-based index of property to upgrade
    def UpgradeProp(self, n):

        self.gm.upgrade_prop(n - 1) # attempt to upgrade the property

        prop = self.gm.properties[n-1] #get property object

        #Since player may have spent currency, update text that tracks current currency
        if (self.endtime - self.gm.time < 10000):   #only display timer if there are less than 10000 seconds Remaining
            document.getElementById('cash').innerHTML = 'Total KitKats: {}<br>Remaining Time : {}'.format(toForm2(self.gm.currency), self.endtime - self.gm.time)
        else:
            document.getElementById('cash').innerHTML = 'Total KitKats: {}'.format(toForm2(self.gm.currency))
        document.getElementById ('prop'+ str(n)) .innerHTML = "You've developed {} {} algorithms. <br>Earning {} {} per second.".format (prop.count, prop.name, toForm2(prop.total_income), currencyName(prop.total_income))

        #Update tooltip giving per-property income info
        document.getElementById('tt' + str(n)).innerHTML = "Each {} algorithm earns {} {} per second".format(prop.name, toForm2(prop.income), currencyName(prop.income))

        ug = prop.get_next_upgrade() #get upgrade object

        #Update tootip with new upgrade, and update upgrade cost text
        document.getElementById('ttu' + str(n)).innerHTML = 'Multipy all {} earnings by {}'.format(prop.name, ug.mult)
        document.getElementById('UC' + str(n)).innerHTML = 'Upgrade : {} KitKats'.format(toForm(ug.cost))


    #Called on penalty button press or key press. Attempt to penalize a property.
    #Params:
    #   n : 1-based index of penalty to use
    def ApplyPenalty(self, n):
        self.gm.applyPenalty(n - 1) #attempt to apply the penalty

        #Update available penalties text
        document.getElementById ('advcount') .innerHTML = 'Available Penalties : {}'.format(self.gm.pen_count)

        prop = self.gm.properties[n-1]

        #update property cost and penalty tooltip
        document.getElementById ('PC'+ str(n)) .innerHTML = 'Cost: {} KitKats'.format (toForm(prop.cost))
        document.getElementById ('tta'+str(n)) .innerHTML = 'Increase cost of {} by a factor of {}'.format(prop.name, self.gm.penalties[n].mult.toFixed(2))

    #Respond to a keypress
    #On press of "1" to "8" keys, call penalty function with appropriate parameter. Otherwise dop nothing
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

    #Called every second through window.setInterval
    def Update (self):
        self.gm.cycle() #Call one game cycle

        #Update currency display, since income is earned every cycle
        if (self.endtime - self.gm.time < 10000):
            document.getElementById('cash').innerHTML = 'Total KitKats: {}<br>Remaining Time : {}'.format(toForm2(self.gm.currency), self.endtime - self.gm.time)
        else:
            document.getElementById('cash').innerHTML = 'Total KitKats: {}'.format(toForm2(self.gm.currency))

        #Update penalty count text sin two player game, since that may have changed
        if self.two_player:
            document.getElementById ('advcount') .innerHTML = 'Available Penalties : {}'.format(self.gm.pen_count)

        #Check if time has expired
        if self.gm.time >= self.endtime:
            self.EndGame()


    #Contains code to setup the screen for a new game
    def Setup(self):

        #Get number from the text box an the start screen
        textbox = document.getElementById("timeSet")
        #Use to set the ending time of the game
        self.endtime = int(textbox.elements[0].value)
        if self.endtime == 0:
            self.endtime = 1000000000

        #Make start screen sections invisible
        document.getElementById("startButtons").style.display = "none"
        document.getElementById("resDiv").style.display = "none"
        document.getElementById("story").style.display = "none"

        #Show currency display and property sections
        document.getElementById("cash").style.display = "inline-block"
        for n in [1,2,3,4,5,6,7,8]:
            document.getElementById("sec" + str(n)).style.display = "inline-block"

        #initialize currency display
        if (self.endtime - self.gm.time < 10000):
            document.getElementById('cash').innerHTML = 'Total KitKats: {}<br>Remaining Time : {}'.format(toForm2(self.gm.currency), self.endtime - self.gm.time)
        else:
            document.getElementById('cash').innerHTML = 'Total KitKats: {}'.format(toForm2(self.gm.currency))


        # In two player game, initialize adversary count text
        if self.two_player:
            document.getElementById ('advcount') .innerHTML = 'Available Penalties : {}'.format(self.gm.pen_count)

        for n in [1,2,3,4,5,6,7,8]:  #for each property
            prop = self.gm.properties[n-1] #get property object
            #Initialize penalty areas tooltips
            if self.two_player:
                document.getElementById ('tta'+str(n)) .innerHTML = 'Increase cost of {} by a factor of {}'.format(prop.name, self.gm.penalties[n-1].mult.toFixed(2))

            #Initialize all property, upgrade, cost, and tooltip text
            document.getElementById ('prop'+ str(n)) .innerHTML = "You've developed {} {} algorithms. <br>Earning {} {} per second.".format (prop.count, prop.name, toForm2(prop.total_income), currencyName(prop.total_income))
            document.getElementById ('PC'+ str(n)) .innerHTML = 'Cost: {} KitKats'.format (toForm(prop.cost))
            document.getElementById('tt' + str(n)).innerHTML = "Each {} algorithm earns {} {} per second".format(prop.name, toForm2(prop.income), currencyName(prop.income))
            ug = prop.get_next_upgrade() #Get upgrade object
            document.getElementById('ttu' + str(n)).innerHTML = 'Multipy all {} earnings by {}'.format(prop.name, ug.mult)
            document.getElementById('UC' + str(n)).innerHTML = 'Upgrade : {} KitKats'.format(toForm(ug.cost))

        #Set the Update() function to run once per second.
        self.inter = window.setInterval(self.Update, 1000)



game = incremental ()
