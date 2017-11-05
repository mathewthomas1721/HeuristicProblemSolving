import numpy as np
import random

EQUAL = 0
GREAT = 1
LESS = 2
INCOMPARABLE = 3


class Random_Poser:
	def __init__(self, nump, numv, numc):
		self.num_packages = nump
		self.num_versions = numv
		self.num_compatibles = numc
		self.compats = 0
		self.compatibility_mat = np.zeros((self.num_packages*self.num_versions, self.num_packages*self.num_versions), dtype=np.int)
		self.compatibility_list = []
		

	def first_config(self):
		config = []
		for p in range(self.num_packages):
			version = random.randint(0,self.num_versions - 1)
			config.append(version)
			for p2 in range(len(config) - 1):
				v2 = config[p2]
				self.compatibility_list.append((p2*self.num_versions + v2,p*self.num_versions + version))
				self.compatibility_mat[p2*self.num_versions + v2, p*self.num_versions + version] = 1
				self.compatibility_mat[p*self.num_versions + version, p2*self.num_versions + v2] = 1
				self.compats += 1
		self.config = config

	def random_compats(self):
		while self.compats < self.num_compatibles:
			pv1 = random.randint(0,self.num_versions * self.num_packages - 1)
			pv2 = random.randint(0,self.num_versions * self.num_packages - 1)
			if (pv1 / self.num_versions == pv2 / self.num_versions):
				continue
			if self.compatibility_mat[pv1, pv2] != 1:
				self.compatibility_mat[pv1, pv2] = 1
				self.compatibility_mat[pv2, pv1] = 1
				self.compatibility_list.append((pv1, pv2))
				self.compats += 1

	def generate_compats(self):
		self.first_config()
		self.random_compats()
		return self.compatibility_list

	def get_CPoser(self):
		return [self.config]





class Solver:

	def __init__(self, nump, numv, numc):
		self.num_packages = nump
		self.num_versions = numv
		self.num_compatibles = numc
		self.compatibility_mat = np.zeros((self.num_packages*self.num_versions, self.num_packages*self.num_versions), dtype=np.int)
		#self.compatibility_list = [[[]] * self.num_packages] * self.num_packages * self.num_versions


	def get_compats(self, compatibility_list):
		for (pv1, pv2) in compatibility_list:
			self.compatibility_mat[pv1, pv2] = 1
			self.compatibility_mat[pv2, pv1] = 1

	def Acceptable(self, config):
		for p1 in range(self.num_packages):
			v1 = config[p1]
			if v1 < 0 or v1 >= self.num_versions:
				return False
		for p1 in range(self.num_packages):
			v1 = config[p1]
			index1 = p1 * self.num_versions + v1
			for p2 in range(self.num_packages):
				v2 = config[p2]
				index2 = p2 * self.num_versions + v2
				if self.compatibility_mat[index1, index2] == 0:
					return False
		return True


	def compare(self,c1, c2):
		state = EQUAL
		for pack in range(self.num_packages):
			if (c1[pack]  > c2[pack]):
				if state == EQUAL:
					state = GREAT
				elif state == LESS:
					return INCOMPARABLE
			elif (c1[pack]  < c2[pack]):
				if state == EQUAL:
					state = LESS
				if state == GREAT:
					return INCOMPARABLE
		return state

	def compare2(self, c1, c2):
		cmp = c1 - c2
		if (not cmp.any()):
			return EQUAL
		pos = (cmp >= 0)
		if (pos).all():
			return GREAT
		if (not pos.any()):
			return LESS
		return INCOMPARABLE


	def backtrack_search_max(self):
		config = np.zeros(self.num_packages, dtype=np.int)
		config.fill(self.num_versions)
		current_pack = 0
		while current_pack < self.num_packages:
			config[current_pack] -= 1
			version = config[current_pack]	
			if version < 0:
				config[current_pack] = self.num_versions
				current_pack -= 1
				if current_pack < 0:
					return -1
				continue
			works = True
			for p in range(current_pack):
				if self.compatibility_mat[current_pack*self.num_versions + version, p*self.num_versions + config[p]] == 0:
					works = False
					break
			if works:
				current_pack += 1
		return config


	"""def set_search(self):
					packages = [[v for v in range(self.num_versions)] for p in range(self.num_packages)]
					current_pack = 0
					while current_pack < self.num_packages
						versions_left = len(packages[current_pack])
						current_version = packages[current_pack][versions_left - 1]"""






s = Solver(20, 40, 10000)
p = Random_Poser(20, 40, 10000)
compats = p.generate_compats()
s.get_compats(compats)
CSolver = [s.backtrack_search_max()]
print(np.array(p.get_CPoser()[0]))
print(CSolver[0])








