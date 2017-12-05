	(function () {
		var base_mult = 1.25;
		var base_pen = 1.5;
		var toForm = function (num) {
			if (num > 1000000) {
				return num.toExponential (3);
			}
			else {
				var round_num = num.toFixed (0);
				if (int (round_num) < num) {
					return (num + 1).toFixed (0);
				}
				else {
					return round_num;
				}
			}
		};
		var toForm2 = function (num) {
			if (num > 1000000) {
				return num.toExponential (3);
			}
			else {
				return num.toFixed (0);
			}
		};
		var currencyName = function (n) {
			if (n == 1) {
				return 'KitKat';
			}
			else {
				return 'KitKats';
			}
		};
		var Property = __class__ ('Property', [object], {
			get __init__ () {return __get__ (this, function (self, py_name, base_cost, cost_mult, base_income) {
				self.py_name = py_name;
				self.cost = base_cost;
				self.mult = cost_mult;
				self.income = base_income;
				self.count = 0.0;
				self.total_income = 0.0;
				self.upgrades_Available = list ([]);
			});},
			get get_income () {return __get__ (this, function (self) {
				return self.income;
			});},
			get inc_cost () {return __get__ (this, function (self) {
				self.cost *= self.mult;
			});},
			get buy () {return __get__ (this, function (self) {
				self.count++;
				self.total_income = self.count * self.income;
			});},
			get get_next_upgrade () {return __get__ (this, function (self) {
				return self.upgrades_Available [0];
			});},
			get upgrade () {return __get__ (this, function (self) {
				var ug = self.upgrades_Available [0];
				self.income *= ug.mult;
				if (len (self.upgrades_Available) == 1) {
					ug.cost *= 10;
				}
				else {
					self.upgrades_Available.py_pop (0);
				}
				self.total_income = self.count * self.income;
			});}
		});
		var Upgrade = __class__ ('Upgrade', [object], {
			get __init__ () {return __get__ (this, function (self, py_name, cost, mult) {
				self.py_name = py_name;
				self.cost = cost;
				self.mult = mult;
			});}
		});
		var Penalty = __class__ ('Penalty', [object], {
			get __init__ () {return __get__ (this, function (self, pen) {
				self.py_name = pen [0];
				if (pen [1] == 0) {
					self.py_metatype = 0;
					self.prop = pen [2];
					self.mult = pen [3];
				}
			});}
		});
		var Game = __class__ ('Game', [object], {
			get __init__ () {return __get__ (this, function (self, props, upgrades) {
				self.counter = 0;
				self.time = 0;
				self.currency = 6.0;
				self.cum_currency = 0.0;
				self.pen_count = 0;
				self.properties = list ([]);
				self.global_multiplier = 1.0;
				var __iterable0__ = props;
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var prop = __iterable0__ [__index0__];
					self.properties.append (Property (prop [0], prop [1], prop [2], prop [3]));
				}
				var __iterable0__ = upgrades;
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var ug = __iterable0__ [__index0__];
					self.properties [ug [1]].upgrades_Available.append (Upgrade (ug [0], ug [2], ug [3]));
				}
			});},
			get buy_prop () {return __get__ (this, function (self, prop_to_buy) {
				var prop = self.properties [prop_to_buy];
				if (self.currency >= prop.cost) {
					self.currency -= prop.cost;
					prop.inc_cost ();
					prop.buy ();
					return true;
				}
				return false;
			});},
			get upgrade_prop () {return __get__ (this, function (self, prop_to_upgrade) {
				var prop = self.properties [prop_to_upgrade];
				var ug = prop.upgrades_Available [0];
				if (self.currency >= ug.cost) {
					self.currency -= ug.cost;
					prop.upgrade ();
					return true;
				}
				return false;
			});},
			get cycle () {return __get__ (this, function (self) {
				self.counter++;
				self.time++;
				var __iterable0__ = self.properties;
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var prop = __iterable0__ [__index0__];
					self.currency += prop.total_income * self.global_multiplier;
					self.cum_currency += prop.total_income * self.global_multiplier;
				}
			});}
		});
		var Two_Player_Game = __class__ ('Two_Player_Game', [Game], {
			get __init__ () {return __get__ (this, function (self, props, upgrades, penalties) {
				Game.__init__ (self, props, upgrades);
				self.penalties = list ([]);
				self.active_penalties = list ([]);
				var __iterable0__ = penalties;
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var pen = __iterable0__ [__index0__];
					self.penalties.append (Penalty (pen));
				}
				var __iterable0__ = self.properties;
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var prop = __iterable0__ [__index0__];
					prop.mult = 1.0;
				}
			});},
			get buy_prop () {return __get__ (this, function (self, prop_to_buy) {
				var succeed = Game.buy_prop (self, prop_to_buy);
				if (succeed) {
					self.counter = 0.0;
					self.pen_count++;
				}
			});},
			get cycle () {return __get__ (this, function (self) {
				Game.cycle (self);
				if (self.counter >= 20) {
					self.pen_count++;
					self.counter = 0;
				}
			});},
			get applyPenalty () {return __get__ (this, function (self, pen_no) {
				if (self.pen_count > 0) {
					self.pen_count--;
					var pen = self.penalties [pen_no];
					if (pen.py_metatype == 0) {
						self.properties [pen.prop].cost *= pen.mult;
					}
				}
			});}
		});
		var incremental = __class__ ('incremental', [object], {
			properties: function () {
				var __accu0__ = [];
				var __iterable0__ = list ([tuple (['Expanding Nim', 6.0, base_mult, 1.0]), tuple (['Stoplight Shortest Path', 50.0, base_mult, 6.0]), tuple (['No Tipping', 400.0, base_mult, 35.0]), tuple (['Gravitational Voronoi', 2000.0, base_mult, 144.0]), tuple (['Evasion', 10000.0, base_mult, 600.0]), tuple (['Dancing Without Stars', 50000.0, base_mult, 2200.0]), tuple (['Compatibility Game', 400000.0, base_mult, 11111.0]), tuple (['Auction Game', 2000000.0, base_mult, 40000.0])]);
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var tupl = __iterable0__ [__index0__];
					__accu0__.append (list (tupl));
				}
				return __accu0__;
			} (),
			upgrades: function () {
				var __accu0__ = [];
				var __iterable0__ = list ([tuple (['Dynamic Programming', 0, 40, 2.0]), tuple (["Dijkstra's Algorithm", 1, 250, 2.0]), tuple (['Dynamic Programming', 2, 3000, 2.0]), tuple (['Clustering', 3, 18000, 2.0]), tuple (['No Diagonal Walls', 4, 80000, 2.0]), tuple (['Simulated Annealing', 5, 500000, 2.0]), tuple (['Depth First Search', 6, 7000000, 2.0]), tuple (['Block Opponents', 7, 33000000, 2.0])]);
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var tupl = __iterable0__ [__index0__];
					__accu0__.append (list (tupl));
				}
				return __accu0__;
			} (),
			penalties: function () {
				var __accu0__ = [];
				var __iterable0__ = list ([tuple (['Cost Increase 1', 0, 0, base_pen]), tuple (['Cost Increase 2', 0, 1, base_pen]), tuple (['Cost Increase 3', 0, 2, base_pen]), tuple (['Cost Increase 4', 0, 3, base_pen]), tuple (['Cost Increase 5', 0, 4, base_pen]), tuple (['Cost Increase 6', 0, 5, base_pen]), tuple (['Cost Increase 7', 0, 6, base_pen]), tuple (['Cost Increase 8', 0, 7, base_pen])]);
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var tupl = __iterable0__ [__index0__];
					__accu0__.append (list (tupl));
				}
				return __accu0__;
			} (),
			get __init__ () {return __get__ (this, function (self) {
				self.endtime = 100000000;
			});},
			get StartOnePlayer () {return __get__ (this, function (self) {
				self.gm = Game (self.properties, self.upgrades);
				self.two_player = false;
				self.Setup ();
			});},
			get StartTwoPlayer () {return __get__ (this, function (self) {
				self.gm = Two_Player_Game (self.properties, self.upgrades, self.penalties);
				window.addEventListener ('keydown', self.respondKey);
				document.getElementById ('ins').style.display = 'inline-block';
				document.getElementById ('adPane').style.display = 'inline-block';
				self.two_player = true;
				self.Setup ();
			});},
			get EndGame () {return __get__ (this, function (self) {
				document.getElementById ('adPane').style.display = 'none';
				document.getElementById ('cash').style.display = 'none';
				document.getElementById ('ins').style.display = 'none';
				var __iterable0__ = list ([1, 2, 3, 4, 5, 6, 7, 8]);
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var n = __iterable0__ [__index0__];
					document.getElementById ('sec' + str (n)).style.display = 'none';
				}
				document.getElementById ('startButtons').style.display = 'inline-block';
				document.getElementById ('resDiv').style.display = 'inline-block';
				document.getElementById ('resDiv').innerHTML = 'Game Over. Player earned {} KitKats in {} seconds.'.format (toForm2 (self.gm.cum_currency), self.endtime);
				window.clearInterval (self.inter);
				window.removeEventListener ('keydown', self.respondKey);
			});},
			get BuyProp () {return __get__ (this, function (self, n) {
				self.gm.buy_prop (n - 1);
				var prop = self.gm.properties [n - 1];
				document.getElementById ('prop' + str (n)).innerHTML = "You've developed {} {} algorithms. <br>Earning {} {} per second.".format (prop.count, prop.py_name, toForm2 (prop.total_income), currencyName (prop.total_income));
				document.getElementById ('PC' + str (n)).innerHTML = 'Cost: {} KitKats'.format (toForm (prop.cost));
				if (self.endtime - self.gm.time < 10000) {
					document.getElementById ('cash').innerHTML = 'Total KitKats: {}<br>Remaining Time : {}'.format (toForm2 (self.gm.currency), self.endtime - self.gm.time);
				}
				else {
					document.getElementById ('cash').innerHTML = 'Total KitKats: {}'.format (toForm2 (self.gm.currency));
				}
				if (self.two_player) {
					document.getElementById ('advcount').innerHTML = 'Available Penalties : {}'.format (self.gm.pen_count);
				}
			});},
			get UpgradeProp () {return __get__ (this, function (self, n) {
				self.gm.upgrade_prop (n - 1);
				var prop = self.gm.properties [n - 1];
				if (self.endtime - self.gm.time < 10000) {
					document.getElementById ('cash').innerHTML = 'Total KitKats: {}<br>Remaining Time : {}'.format (toForm2 (self.gm.currency), self.endtime - self.gm.time);
				}
				else {
					document.getElementById ('cash').innerHTML = 'Total KitKats: {}'.format (toForm2 (self.gm.currency));
				}
				document.getElementById ('prop' + str (n)).innerHTML = "You've developed {} {} algorithms. <br>Earning {} {} per second.".format (prop.count, prop.py_name, toForm2 (prop.total_income), currencyName (prop.total_income));
				document.getElementById ('tt' + str (n)).innerHTML = 'Each {} algorithm earns {} {} per second'.format (prop.py_name, toForm2 (prop.income), currencyName (prop.income));
				var ug = prop.get_next_upgrade ();
				document.getElementById ('ttu' + str (n)).innerHTML = 'Multipy all {} earnings by {}'.format (prop.py_name, ug.mult);
				document.getElementById ('UC' + str (n)).innerHTML = 'Upgrade : {} KitKats'.format (toForm (ug.cost));
			});},
			get ApplyPenalty () {return __get__ (this, function (self, n) {
				self.gm.applyPenalty (n - 1);
				document.getElementById ('advcount').innerHTML = 'Available Penalties : {}'.format (self.gm.pen_count);
				var prop = self.gm.properties [n - 1];
				document.getElementById ('PC' + str (n)).innerHTML = 'Cost: {} KitKats'.format (toForm (prop.cost));
				document.getElementById ('tta' + str (n)).innerHTML = 'Increase cost of {} by a factor of {}'.format (prop.py_name, self.gm.penalties [n].mult.toFixed (2));
			});},
			get respondKey () {return __get__ (this, function (self, event) {
				self.keyCode = event.keyCode;
				if (self.keyCode == ord ('1')) {
					self.ApplyPenalty (1);
				}
				else if (self.keyCode == ord ('2')) {
					self.ApplyPenalty (2);
				}
				else if (self.keyCode == ord ('3')) {
					self.ApplyPenalty (3);
				}
				else if (self.keyCode == ord ('4')) {
					self.ApplyPenalty (4);
				}
				else if (self.keyCode == ord ('5')) {
					self.ApplyPenalty (5);
				}
				else if (self.keyCode == ord ('6')) {
					self.ApplyPenalty (6);
				}
				else if (self.keyCode == ord ('7')) {
					self.ApplyPenalty (7);
				}
				else if (self.keyCode == ord ('8')) {
					self.ApplyPenalty (8);
				}
			});},
			get Update () {return __get__ (this, function (self) {
				self.gm.cycle ();
				if (self.endtime - self.gm.time < 10000) {
					document.getElementById ('cash').innerHTML = 'Total KitKats: {}<br>Remaining Time : {}'.format (toForm2 (self.gm.currency), self.endtime - self.gm.time);
				}
				else {
					document.getElementById ('cash').innerHTML = 'Total KitKats: {}'.format (toForm2 (self.gm.currency));
				}
				if (self.two_player) {
					document.getElementById ('advcount').innerHTML = 'Available Penalties : {}'.format (self.gm.pen_count);
				}
				if (self.gm.time >= self.endtime) {
					self.EndGame ();
				}
			});},
			get Setup () {return __get__ (this, function (self) {
				var textbox = document.getElementById ('timeSet');
				self.endtime = int (textbox.elements [0].value);
				if (self.endtime == 0) {
					self.endtime = 1000000000;
				}
				document.getElementById ('startButtons').style.display = 'none';
				document.getElementById ('resDiv').style.display = 'none';
				document.getElementById ('story').style.display = 'none';
				document.getElementById ('cash').style.display = 'inline-block';
				var __iterable0__ = list ([1, 2, 3, 4, 5, 6, 7, 8]);
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var n = __iterable0__ [__index0__];
					document.getElementById ('sec' + str (n)).style.display = 'inline-block';
				}
				if (self.endtime - self.gm.time < 10000) {
					document.getElementById ('cash').innerHTML = 'Total KitKats: {}<br>Remaining Time : {}'.format (toForm2 (self.gm.currency), self.endtime - self.gm.time);
				}
				else {
					document.getElementById ('cash').innerHTML = 'Total KitKats: {}'.format (toForm2 (self.gm.currency));
				}
				if (self.two_player) {
					document.getElementById ('advcount').innerHTML = 'Available Penalties : {}'.format (self.gm.pen_count);
				}
				var __iterable0__ = list ([1, 2, 3, 4, 5, 6, 7, 8]);
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var n = __iterable0__ [__index0__];
					var prop = self.gm.properties [n - 1];
					if (self.two_player) {
						document.getElementById ('tta' + str (n)).innerHTML = 'Increase cost of {} by a factor of {}'.format (prop.py_name, self.gm.penalties [n - 1].mult.toFixed (2));
					}
					document.getElementById ('prop' + str (n)).innerHTML = "You've developed {} {} algorithms. <br>Earning {} {} per second.".format (prop.count, prop.py_name, toForm2 (prop.total_income), currencyName (prop.total_income));
					document.getElementById ('PC' + str (n)).innerHTML = 'Cost: {} KitKats'.format (toForm (prop.cost));
					document.getElementById ('tt' + str (n)).innerHTML = 'Each {} algorithm earns {} {} per second'.format (prop.py_name, toForm2 (prop.income), currencyName (prop.income));
					var ug = prop.get_next_upgrade ();
					document.getElementById ('ttu' + str (n)).innerHTML = 'Multipy all {} earnings by {}'.format (prop.py_name, ug.mult);
					document.getElementById ('UC' + str (n)).innerHTML = 'Upgrade : {} KitKats'.format (toForm (ug.cost));
				}
				self.inter = window.setInterval (self.Update, 1000);
			});}
		});
		var game = incremental ();
		__pragma__ ('<all>')
			__all__.Game = Game;
			__all__.Penalty = Penalty;
			__all__.Property = Property;
			__all__.Two_Player_Game = Two_Player_Game;
			__all__.Upgrade = Upgrade;
			__all__.base_mult = base_mult;
			__all__.base_pen = base_pen;
			__all__.currencyName = currencyName;
			__all__.game = game;
			__all__.incremental = incremental;
			__all__.toForm = toForm;
			__all__.toForm2 = toForm2;
		__pragma__ ('</all>')
	}) ();
