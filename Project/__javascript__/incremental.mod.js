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
		var Player = __class__ ('Player', [object], {
			get __init__ () {return __get__ (this, function (self, props, upgrades) {
				self.currency = 10.0;
				self.properties = list ([]);
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
				var __iterable0__ = self.properties;
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var prop = __iterable0__ [__index0__];
					self.currency += prop.total_income;
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
			get __init__ () {return __get__ (this, function (self) {
				window.setInterval (self.Update, 500);
				self.player = Player (self.properties, self.upgrades);
			});},
			get BuyProp () {return __get__ (this, function (self, n) {
				self.player.buy_prop (n - 1);
				var prop = self.player.properties [n - 1];
				document.getElementById ('prop' + str (n)).innerHTML = 'You own {} {}s. Cost for next: {}'.format (prop.count, prop.py_name, int (prop.cost));
				document.getElementById ('cash').innerHTML = 'Total Cash: {}'.format (int (self.player.currency));
			});},
			get UpgradeProp () {return __get__ (this, function (self, n) {
				self.player.upgrade_prop (n - 1);
				document.getElementById ('cash').innerHTML = 'Total Cash: {}'.format (int (self.player.currency));
			});},
			get Update () {return __get__ (this, function (self) {
				self.player.cycle ();
				document.getElementById ('cash').innerHTML = 'Total Cash: {}'.format (int (self.player.currency));
				var __iterable0__ = list ([1, 2, 3, 4, 5, 6, 7, 8]);
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var n = __iterable0__ [__index0__];
					var prop = self.player.properties [n - 1];
					document.getElementById ('prop' + str (n)).innerHTML = 'You own {} {}s. Cost for next: {}'.format (prop.count, prop.py_name, int (prop.cost));
				}
			});}
		});
		var game = incremental ();
		__pragma__ ('<all>')
			__all__.Player = Player;
			__all__.Property = Property;
			__all__.Upgrade = Upgrade;
			__all__.game = game;
			__all__.incremental = incremental;
		__pragma__ ('</all>')
	}) ();
