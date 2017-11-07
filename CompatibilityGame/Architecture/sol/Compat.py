import numpy as np
import random
import math
import copy
import time

EQUAL = 0
GREAT = 1
LESS = 2
INCOMPARABLE = 3


class Random_Poser:
	def __init__(self, nump, numv, numc):
		self.num_packages = nump
		self.num_versions = numv
		self.num_compatibles = numc
		if self.num_compatibles >= 0.4 * ((self.num_packages - 1)  * self.num_versions) ** 2:
			self.num_compatibles = int (0.4 * ((self.num_packages - 1 )* self.num_versions) ** 2)
		self.compats = 0
		self.compatibility_mat = np.zeros((self.num_packages*self.num_versions, self.num_packages*self.num_versions), dtype=np.int)
		self.compatibility_list = []


	def first_config(self):
		config = []
		self.config = []
		for p in range(self.num_packages):
			version = random.randint(0,self.num_versions - 1)
			config.append(version)
			for p2 in range(len(config) - 1):
				v2 = config[p2]
				self.compatibility_list.append((p2*self.num_versions + v2,p*self.num_versions + version))
				self.compatibility_mat[p2*self.num_versions + v2, p*self.num_versions + version] = 1
				self.compatibility_mat[p*self.num_versions + version, p2*self.num_versions + v2] = 1
				self.compats += 1

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
		self.backtrack_search_max()
		return self.config

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
				if (p1 != p2) and self.compatibility_mat[index1, index2] == 0:
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


	def backtrack_search_max(self):
		config = np.zeros(self.num_packages, dtype=np.int)
		config.fill(self.num_versions)
		current_pack = 0
		while True:
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
			current_pack -= 1
			(self.config).append(copy.deepcopy(config))

	def generate_output(self):
		print(len(self.compatibility_list))
		for (pv1, pv2) in self.compatibility_list:
			p1 = int(pv1 / self.num_versions)
			v1 = pv1 % self.num_versions
			p2 = int(pv2 / self.num_versions)
			v2 = pv2 % self.num_versions
			print(p1 + 1, v1 + 1, p2 + 1, v2 + 1)
		print(len(self.config))
		for config in self.config:
			out_config = [v + 1 for v in config]
			s = " ".join(map(str,out_config))
			print(s)


class Evil_Poser(Random_Poser):
	def first_config(self):
		self.config = []
		config = [0 for i in range(self.num_packages)]
		for p in range(self.num_packages):
			version = 0
			for p2 in range(p):
				v2 = 0
				self.compatibility_list.append((p2*self.num_versions + v2,p*self.num_versions + version))
				self.compatibility_mat[p2*self.num_versions + v2, p*self.num_versions + version] = 1
				self.compatibility_mat[p*self.num_versions + version, p2*self.num_versions + v2] = 1
				self.compats += 1
		self.config.append(config)

	def box_compats(self):
		compats_left = self.num_compatibles - self.compats
		#print(compats_left)
		k = 2 * compats_left / (self.num_versions ** 2)
		#print(k)
		k = int(math.sqrt(k))
		#print(k)
		for p1 in range(k):
			for p2 in range(k):
				if p1 != p2:
					for v1 in range(self.num_versions):
						for v2 in range(self.num_versions):
							if self.compatibility_mat[p1*self.num_versions + v1, p2*self.num_versions + v2] == 0:
								self.compatibility_mat[p1*self.num_versions + v1, p2*self.num_versions + v2] = 1
								self.compatibility_mat[p2*self.num_versions + v2, p1*self.num_versions + v1] = 1
								self.compatibility_list.append((p2*self.num_versions + v2, p1*self.num_versions + v1))
								self.compats += 1
		#print(self.compats)

	def generate_compats(self):
		self.first_config()
		self.box_compats()
		return self.compatibility_list

	def get_CPoser(self):
		#print(self.config)
		return self.config

class Eviler_Poser(Evil_Poser):
	def first_config(self):
		compats_left = self.num_compatibles - ((self.num_packages * (self.num_packages - 1)) / 2)
		self.k = 2 * compats_left / (self.num_packages * (self.num_packages - 1))
		self.k = int(math.sqrt(self.k))
		#print(self.k)
		self.config = []
		config = [random.randint(0, int(self.k / 2)) for i in range(self.num_packages)]
		for p in range(self.num_packages):
			version = config[p]
			for p2 in range(p):
				v2 = config[p2]
				self.compatibility_list.append((p2*self.num_versions + v2,p*self.num_versions + version))
				self.compatibility_mat[p2*self.num_versions + v2, p*self.num_versions + version] = 1
				self.compatibility_mat[p*self.num_versions + version, p2*self.num_versions + v2] = 1
				self.compats += 1
		self.config.append(config)

	def box_compats(self):
		gap = random.randint(int(self.num_packages / 2),self.num_packages - 2)
		#print(gap)
		for p1 in range(self.num_packages):
			for p2 in range(p1):
				if p1 != gap and p2 != gap:
					for v1 in range(self.k):
						for v2 in range(self.k):
							if self.compatibility_mat[p1*self.num_versions + v1, p2*self.num_versions + v2] == 0:
								self.compatibility_mat[p1*self.num_versions + v1, p2*self.num_versions + v2] = 1
								self.compatibility_mat[p2*self.num_versions + v2, p1*self.num_versions + v1] = 1
								self.compatibility_list.append((p2*self.num_versions + v2, p1*self.num_versions + v1))
								self.compats += 1
				elif p1 == gap:
					if self.k <= self.num_versions / 2:
						for v1 in range(self.k):
							for v2 in range(self.k):
								if self.compatibility_mat[p1*self.num_versions + v1 + self.k, p2*self.num_versions + v2] == 0:
									self.compatibility_mat[p1*self.num_versions + v1 + self.k, p2*self.num_versions + v2] = 1
									self.compatibility_mat[p2*self.num_versions + v2, p1*self.num_versions + v1 + self.k] = 1
									self.compatibility_list.append((p2*self.num_versions + v2, p1*self.num_versions + v1 + self.k))
									self.compats += 1
				else:
					if self.k <= self.num_versions / 3:
						for v1 in range(self.k):
							for v2 in range(self.k):
								if self.compatibility_mat[p1*self.num_versions + v1, p2*self.num_versions + v2 + 2 * self.k] == 0:
									self.compatibility_mat[p1*self.num_versions + v1, p2*self.num_versions + v2 + 2 * self.k] = 1
									self.compatibility_mat[p2*self.num_versions + v2 + 2 * self.k, p1*self.num_versions + v1] = 1
									self.compatibility_list.append((p2*self.num_versions + v2  + 2 * self.k, p1*self.num_versions + v1))
									self.compats += 1
					else:
						for v1 in range(self.k):
							for v2 in range(self.k):
								if self.compatibility_mat[p1*self.num_versions + v1  + self.k, p2*self.num_versions + v2] == 0:
									self.compatibility_mat[p1*self.num_versions + v1 + self.k, p2*self.num_versions + v2] = 1
									self.compatibility_mat[p2*self.num_versions + v2, p1*self.num_versions + v1  + self.k] = 1
									self.compatibility_list.append((p2*self.num_versions + v2, p1*self.num_versions + v1 + self.k))
									self.compats += 1


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
				if (p1 != p2) and self.compatibility_mat[index1, index2] == 0:
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
			#print(config[:current_pack+1])
			works = True
			for p in range(current_pack):
				if self.compatibility_mat[current_pack*self.num_versions + version, p*self.num_versions + config[p]] == 0:
					works = False
					break
			if works:
				current_pack += 1
		return config


	def set_search(self):
		packages = [[v for v in range(self.num_versions)] for p in range(self.num_packages)]
		perm = np.random.permutation(self.num_packages)
		invperm = np.zeros(self.num_packages, dtype = np.int)
		for i, p in enumerate(perm):
			invperm[p] = i
		backtrack = [[]] * self.num_packages
		backtrack[0] = copy.deepcopy(packages)
		current_pack = 0
		t = time.clock()
		timeout = False
		while current_pack < self.num_packages:
			if (time.clock() - t > 5):
				timeout = True
				break
			backtrack[current_pack] = copy.deepcopy(packages)
			versions_left = len(packages[current_pack])
			if versions_left == 0:
				current_pack -= 1
				if current_pack < 0:
					return -1
				packages = backtrack[current_pack]
				packages[current_pack].remove(len(packages[current_pack]) - 1)
				continue
			current_version = packages[current_pack][versions_left - 1]
			index1 = perm[current_pack] * self.num_versions + current_version
			#print([packages[p][len(packages[p]) - 1] for p in range(current_pack + 1)])
			possible = True
			for p in range (current_pack + 1, self.num_packages):

				packages[p] = [version for version in packages[p] if self.compatibility_mat[index1, perm[p]*self.num_versions + version] == 1]
				if not packages[p]:
					possible = False
					break
			if not possible:
				packages = backtrack[current_pack]
				packages[current_pack].remove(current_version)
			else:
				 current_pack += 1
		if timeout:
			#print("restart")
			return self.set_search()
		else:
			return [packages[invperm[p]][len(packages[invperm[p]]) - 1] for p in range(self.num_packages)]


	def parse_compats(self, g):
		compats = []
		for c in g:
			compats.append(((c[0] - 1) * self.num_versions + (c[1] - 1),(c[2] - 1) * self.num_versions + (c[3] - 1)) )
		self.get_compats(compats)

	def generate_output(self, CSolver):
		print(1)
		solution = [v + 1 for v in CSolver]
		print(' '.join(map(str,solution)))







"""
print(time.clock())
s = Solver(20, 40 , 10000)
p = Eviler_Poser(20, 40, 10000)
compats = p.generate_compats()
s.get_compats(compats)
CSolver = [s.set_search()]
#CSolver = [s.backtrack_search_max()]
print(p.get_CPoser())
print(CSolver)
print(time.clock())

"""
