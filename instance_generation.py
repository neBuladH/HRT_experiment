import random
import numpy as np

class Formation:
	def __init__(self, nb_places, popularite, identifiant):
		self.id = identifiant
		self.nb_places = nb_places
		self.popularite = popularite
		self.candidatures = []
		self.nb_candidats = 0

	def __str__(self):
		return "Formation " + str(self.id) + " : " + str(self.nb_places) + " places, popularite : " + str(self.popularite) + ", " + str(len(self.candidatures)) + " candidats"

	def __repr__(self):
		return "Formation " + str(self.id) + " (" + str(self.popularite) + ")"

class Candidat:
	def __init__(self, popularite, identifiant):
		self.id = identifiant
		self.popularite = popularite
		self.voeux = []
		self.nb_voeux = 0

	def __str__(self):
		return "Candidat " + str(self.id) + ", popularite : " + str(self.popularite)

	def __repr__(self):
		return "Candidat " + str(self.id) + ", pop = " + str(self.popularite)


def generer_formations(nb_f,nb_c):
	formations = [None] * nb_f
	cpt = 0
	total_pop = 0
	for i in range(nb_f):
		popularite = np.floor(max(0, np.random.normal(loc=50,scale=10)))

		capacite = int(np.floor(max(10, np.random.normal(loc=nb_c/nb_f, scale=40))))
		cpt += capacite
		formations[i] = Formation(capacite,popularite,i)
		total_pop += popularite

	#print(cpt)

	while cpt > nb_c:
		r = random.randrange(nb_f)
		if formations[r].nb_places > 1:
			formations[r].nb_places -= 1
			cpt -= 1
	while cpt < nb_c:
		r = random.randrange(nb_f)
		formations[r].nb_places += 1
		cpt += 1

	#print(cpt)
	#print([f.nb_places for f in formations])

	#for i in range(nb_f):
		#print(formations[i])
	return formations, total_pop


def generer_candidats(nb):
	candidats = [None] * nb
	for i in range(nb):
		popularite = np.floor(max(1, np.random.normal(loc=50,scale=15)))
		candidats[i] = Candidat(popularite, i)
		#print(candidats[i])

	return candidats
	

def etablir_voeux(candidats, formations, total_pop, nb_voeux_moy):

	for c in candidats:
		nb_voeux = int(np.floor(max(2, np.random.normal(loc=nb_voeux_moy))))

		c.voeux = [None] * nb_voeux

		print(c.id)

		i = 0
		while i < nb_voeux:
			cpt = 0 ; j = 0
			r = random.uniform(0,1)
			#print("=====")
			#print(nb_voeux)
			#print(r)
			while j < len(formations) -1 and r > cpt + formations[j].popularite/total_pop :
				#print(nb_voeux)
				cpt += formations[j].popularite/total_pop
				j += 1
				#print(cpt)
			if formations[j] not in c.voeux:
				c.voeux[i] = formations[j]
				formations[j].candidatures.append(c)
				i += 1
		#print(c.voeux)
		c.nb_voeux = len(c.voeux)

	#for f in formations:
		#print(f)

	return 0

def tri_candidatures(formations):

	for f in formations:
		#print(f.candidatures)
		cand_tries = [None] * len(f.candidatures)
		popularite_candidats = sum([c.popularite for c in f.candidatures])
		for c in range(len(f.candidatures)):
			r = random.uniform(0,1) ; i = 0 ; cpt = 0
			while i < len(f.candidatures) - 1 and r > cpt + f.candidatures[i].popularite/popularite_candidats:
				i += 1
				cpt += f.candidatures[i].popularite/popularite_candidats

			popularite_candidats -= f.candidatures[i].popularite
			cand_tries[c] = f.candidatures.pop(i)
		print(f.id)
		f.candidatures = cand_tries
		f.nb_candidats = len(f.candidatures)
		#print(f.candidatures)
	return 0

def generer_egalites(candidats, p):
	for c in candidats:
		liste_voeux = [None] * len(c.voeux)
		rang = 1
		for i in range(len(c.voeux)):
			r = random.uniform(0,1)
			liste_voeux[i] = (c.voeux[i], rang)
			if r > p:
				rang += 1

		c.voeux = liste_voeux
	return 0

def generate_instance(nb_formations = 100, nb_candidats = 10000, nb_voeux_moy = 8, p_ties = 0.05, nb_instances = 1, d = "instances"):

	noms_fichiers = [None] * nb_instances

	for i in range(nb_instances):

		formations, popularite_totale = generer_formations(nb_f=nb_formations, nb_c=nb_candidats)

		candidats = generer_candidats(nb_candidats)

		etablir_voeux(candidats, formations, popularite_totale, nb_voeux_moy)

		tri_voeux(candidats)

		tri_candidatures(formations)

		generer_egalites(candidats, p_ties)

		nom_fichier = generer_fichier(formations, candidats, p_ties*100, nb_voeux_moy, i+1, d)
		noms_fichiers[i] = nom_fichier

		print(nom_fichier)

	return noms_fichiers

	#return candidats, formations

def exemple_rapport():
	c_0 = Candidat(0,0)
	c_1 = Candidat(0,1)
	c_2 = Candidat(0,2)
	c_3 = Candidat(0,3)
	c_4 = Candidat(0,4)
	c_5 = Candidat(0,5)

	candidats = [c_0,c_1,c_2,c_3,c_4,c_5]

	f_0 = Formation(1,5,0)
	f_1 = Formation(1,4,1)
	f_2 = Formation(2,2,2)
	f_3 = Formation(2,2,3)
	candidats[0].voeux = [(f_0,1),(f_1,1),(f_2,2)]
	candidats[1].voeux = [(f_1,1),(f_3,2)]
	candidats[2].voeux = [(f_2,1),(f_3,1)]
	candidats[3].voeux = [(f_0,1),(f_1,2)]
	candidats[4].voeux = [(f_1,1),(f_2,1)]
	candidats[5].voeux = [(f_0,1),(f_2,2)]

	formations = [f_0,f_1,f_2,f_3]

	formations[0].candidatures = [c_0,c_3,c_5]
	formations[1].candidatures = [c_0, c_1, c_3, c_4]
	formations[2].candidatures = [c_0, c_2, c_4, c_5]
	formations[3].candidatures = [c_1,c_2]

	return candidats, formations

def generer_fichier(formations, candidats, p_ties, nb_voeux, i = 1, directory = "instances"):

	nom_fichier = directory + "/" + str(len(formations)) + "_" + str(len(candidats)) + "_" + str(int(p_ties)) + "_" + str(nb_voeux) + "_" + str(i) + ".txt"
	#nom_fichier = "instances/exemple_rapport.txt"
	fichier = open(nom_fichier, "w")

	fichier.write(str(len(formations)) + '\n')
	fichier.write(str(len(candidats)) + '\n')

	for f in formations:
		fichier.write(str(f.nb_places) + ' ' + str(int(f.popularite)) + '\n')

	for c in candidats:
		fichier.write(str(int(c.popularite)) + '\n')

	for f in formations:
		for c in f.candidatures:
			fichier.write(str(c.id) + ' ')
		fichier.write('\n')

	for c in candidats:
		for v in c.voeux:
			fichier.write(str(v[1]) + ':' + str(v[0].id) + ' ')
		fichier.write('\n')
	fichier.close()

	return nom_fichier

def parser_fichier(nom_fichier):

	fichier = open(nom_fichier, "r")

	nb_formations = int(fichier.readline())
	formations = [None] * nb_formations

	nb_candidats = int(fichier.readline())
	candidats = [None] * nb_candidats

	for i in range(nb_formations):
		valeurs = fichier.readline().split(" ")

		popularite = int(valeurs[1])
		nb_places = int(valeurs[0])
		formations[i] = Formation(nb_places, popularite, i)

	for i in range(nb_candidats):
		popularite = int(fichier.readline())

		candidats[i] = Candidat(popularite, i)

	for i in range(nb_formations):
		candidatures = fichier.readline().split(" ")[:-1]
		formations[i].nb_candidats = len(candidatures)
		formations[i].candidatures = [candidats[int(c)] for c in candidatures]

	for i in range(nb_candidats):
		voeux = fichier.readline().split(" ")[:-1]
		for j in range(len(voeux)):
			voeux[j] = voeux[j].split(":")
		candidats[i].nb_voeux = len(voeux)
		candidats[i].voeux = [(formations[int(v[1])], int(v[0])) for v in voeux]

	#print([f.candidatures for f in formations])
	#print([c.voeux for c in candidats])

	return candidats, formations