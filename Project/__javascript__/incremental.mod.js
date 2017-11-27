	(function () {
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
			get upgrade () {return __get__ (this, function (self) {
				var ug = self.upgrades_Available.py_pop (0);
				self.income *= ug.mult;
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
				else if (pen [1] == 1) {
					self.py_metatype = 1;
					self.mult = pen [2];
					self.duration = pen [3];
					self.time_left = self.duration;
				}
				else {
					self.py_name = 'Florg';
				}
			});}
		});
		var Game = __class__ ('Game', [object], {
			get __init__ () {return __get__ (this, function (self, props, upgrades) {
				self.counter = 0;
				self.currency = 10.0;
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
				var __iterable0__ = self.properties;
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var prop = __iterable0__ [__index0__];
					self.currency += prop.total_income * self.global_multiplier;
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
					self.pen_count++;
				}
			});},
			get cycle () {return __get__ (this, function (self) {
				Game.cycle (self);
				if (__mod__ (self.counter, 25) == 0) {
					self.pen_count++;
				}
				var new_active = self.active_penalties;
				self.active_penalties = list ([]);
				var __iterable0__ = self.active_penalties;
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var pen = __iterable0__ [__index0__];
					pen.time_left--;
					if (pen.time_left == 0) {
						self.global_multiplier *= 1.0 / pen.mult;
						pen.time_left = pen.duration;
					}
					else {
						self.active_penalties.append (pen);
					}
				}
			});},
			get applyPenalty () {return __get__ (this, function (self, pen_no) {
				if (self.pen_count > 0) {
					self.pen_count--;
					var pen = self.penalties [pen_no];
					pen.py_name = 'florg1';
					if (pen.py_metatype == 0) {
						self.properties [pen.prop].cost *= pen.mult;
					}
					else if (pen.py_metatype == 1) {
						self.active_penalties.append (pen);
						self.global_multiplier *= pen.mult;
					}
				}
			});}
		});
		var incremental = __class__ ('incremental', [object], {
			properties: function () {
				var __accu0__ = [];
				var __iterable0__ = list ([tuple (['Burger Stand', 10.0, 1.15, 1.0]), tuple (['Diner', 100.0, 1.15, 8.0]), tuple (['Gas Station', 1000.0, 1.15, 60.0]), tuple (['Wal-Mart', 8000.0, 1.15, 420.0]), tuple (['Bank', 65000.0, 1.15, 2500.0]), tuple (['Department Store', 210000.0, 1.15, 9000.0]), tuple (['Auto Manufacturer', 4000000.0, 1.15, 100000.0]), tuple (['Conglomerate', 100000000.0, 1.15, 2000000.0])]);
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var tupl = __iterable0__ [__index0__];
					__accu0__.append (list (tupl));
				}
				return __accu0__;
			} (),
			upgrades: function () {
				var __accu0__ = [];
				var __iterable0__ = list ([tuple (['Upgrade 1', 0, 10, 2.0]), tuple (['Upgrade 1', 1, 10, 2.0]), tuple (['Upgrade 1', 2, 10, 2.0]), tuple (['Upgrade 1', 3, 10, 2.0]), tuple (['Upgrade 1', 4, 10, 2.0]), tuple (['Upgrade 1', 5, 10, 2.0]), tuple (['Upgrade 1', 6, 10, 2.0]), tuple (['Upgrade 1', 7, 10, 2.0]), tuple (['Upgrade 1', 0, 10, 2.0]), tuple (['Upgrade 1', 1, 10, 2.0]), tuple (['Upgrade 1', 2, 10, 2.0]), tuple (['Upgrade 1', 3, 10, 2.0]), tuple (['Upgrade 1', 4, 10, 2.0]), tuple (['Upgrade 1', 5, 10, 2.0]), tuple (['Upgrade 1', 6, 10, 2.0]), tuple (['Upgrade 1', 7, 10, 2.0]), tuple (['Upgrade 1', 0, 10, 2.0]), tuple (['Upgrade 1', 1, 10, 2.0])]);
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var tupl = __iterable0__ [__index0__];
					__accu0__.append (list (tupl));
				}
				return __accu0__;
			} (),
			penalties: function () {
				var __accu0__ = [];
				var __iterable0__ = list ([tuple (['Cost Increase 1', 0, 0, 1.15]), tuple (['Cost Increase 2', 0, 1, 1.15]), tuple (['Cost Increase 3', 0, 2, 1.15]), tuple (['Cost Increase 4', 0, 3, 1.15]), tuple (['Cost Increase 5', 0, 4, 1.15]), tuple (['Cost Increase 6', 0, 5, 1.15]), tuple (['Cost Increase 7', 0, 6, 1.15]), tuple (['Cost Increase 8', 0, 7, 1.15]), tuple (['Penalty 1', 1, 0.5, 100])]);
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var tupl = __iterable0__ [__index0__];
					__accu0__.append (list (tupl));
				}
				return __accu0__;
			} (),
			get __init__ () {return __get__ (this, function (self, two_player) {
				window.setInterval (self.Update, 500);
				if (two_player) {
					self.gm = Two_Player_Game (self.properties, self.upgrades, self.penalties);
				}
				else {
					self.gm = Game (self.properties, self.upgrades);
				}
			});},
			get BuyProp () {return __get__ (this, function (self, n) {
				self.gm.buy_prop (n - 1);
				var prop = self.gm.properties [n - 1];
				document.getElementById ('prop' + str (n)).innerHTML = 'You own {} {}s. Cost for next: {}'.format (prop.count, prop.py_name, int (prop.cost));
				document.getElementById ('cash').innerHTML = 'Total Cash: {}'.format (int (self.gm.currency));
			});},
			get UpgradeProp () {return __get__ (this, function (self, n) {
				self.gm.upgrade_prop (n - 1);
				document.getElementById ('cash').innerHTML = 'Total Cash: {}'.format (int (self.gm.currency));
			});},
			get ApplyPenalty () {return __get__ (this, function (self, n) {
				self.gm.applyPenalty (n - 1);
				document.getElementById ('adv1').innerHTML = 'Adversary has {} penalties to apply. Next Penalty {}.'.format (self.gm.pen_count, self.gm.penalties [0].py_name);
				var __iterable0__ = list ([1, 2, 3, 4, 5, 6, 7, 8]);
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var n = __iterable0__ [__index0__];
					var prop = self.gm.properties [n - 1];
					document.getElementById ('prop' + str (n)).innerHTML = 'You own {} {}s. Cost for next: {}'.format (prop.count, prop.py_name, int (prop.cost));
				}
			});},
			get Update () {return __get__ (this, function (self) {
				self.gm.cycle ();
				document.getElementById ('cash').innerHTML = 'Total Cash: {}'.format (int (self.gm.currency));
				document.getElementById ('adv1').innerHTML = 'Adversary has {} penalties to apply. Next Penalty {}.'.format (self.gm.pen_count, self.gm.penalties [0].py_name);
				var __iterable0__ = list ([1, 2, 3, 4, 5, 6, 7, 8]);
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var n = __iterable0__ [__index0__];
					var prop = self.gm.properties [n - 1];
					document.getElementById ('prop' + str (n)).innerHTML = 'You own {} {}s. Cost for next: {}'.format (prop.count, prop.py_name, int (prop.cost));
				}
			});}
		});
		var game = incremental (true);
		__pragma__ ('<all>')
			__all__.Game = Game;
			__all__.Penalty = Penalty;
			__all__.Property = Property;
			__all__.Two_Player_Game = Two_Player_Game;
			__all__.Upgrade = Upgrade;
			__all__.game = game;
			__all__.incremental = incremental;
		__pragma__ ('</all>')
	}) ();
