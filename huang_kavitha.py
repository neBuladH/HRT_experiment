import instance_generation as ig
import numpy as np
import random
import sys
from copy import deepcopy

class Noeud:
	def __init__(self, id, arcs):
		self.id = id
		self.arcs = arcs

	def __str__(self):
		return "noeud " + str(self.id) + " (voisins : " + self.voisins + ")"

	def __repr__(self):
		return "noeud " + str(self.id)

class Arc:
	def __init__(self, dest, flot, capacite):
		self.dest = dest
		self.flot = flot
		self.capacite = capacite

	def __str__(self):
		return "vers " + str(self.dest) + " (" + str(self.flot) + "/" + str(self.capacite) + ")"

	def __repr__(self):
		return "vers " + str(self.dest) + " (" + str(self.flot) + "/" + str(self.capacite) + ")"

def moins_desirable(candidat, prop_1, prop_2, rejets, promotion):
	rang_1 = rang_2 = 0
	for v in candidat.voeux:
		#print(v)
		if v[0] == prop_1[0]:
			rang_1 = v[1]
		if v[0] == prop_2[0]:
			rang_2 = v[1]


	if rang_1 > rang_2:
		#print(prop_2, "est mieux classé que", prop_1, "(rangs :",rang_1, "contre", rang_2,")")
		return prop_1
	elif rang_1 < rang_2:
		#print(prop_1, "est mieux classé que", prop_2, "(rangs :",rang_2, "contre", rang_1,")")
		return prop_2
	else:
		#print(prop_1, "et", prop_2, "de même rang")
		if promotion[prop_1[0].id] > promotion[prop_2[0].id]:
			#print("formation", prop_1[0].id, "est mieux promue que formation",prop_2[0].id)
			return prop_2
		elif promotion[prop_1[0].id] < promotion[prop_2[0].id]:
			#print("formation", prop_2[0].id, "est mieux promue que formation",prop_1[0].id)
			return prop_1
		else:
			#print(prop_1, "et", prop_2, "sont à la meme promotion")
			#print(rejets[prop_1[0].id])
			#print(rejets[prop_2[0].id])
			if candidat in rejets[prop_1[0].id]:
				#print(candidat, " a déjà rejetté formation", prop_1[0].id)
				#print(rejets[prop_1[0].id])
				return prop_2
			elif candidat in rejets[prop_2[0].id]:
				#print(candidat, " a déjà rejetté formation", prop_2[0].id)
				#print(rejets[prop_2[0].id])
				return prop_1
			else:
				#print("Aucun n'a déjà été rejeté par candidat", candidat.id)
				return prop_1


def rejette_moins_desirable(candidat, propositions, rejets, promotion):

	p_1 = moins_desirable(candidat, propositions[0], propositions[1], rejets, promotion)
	p_2 = moins_desirable(candidat, p_1, propositions[2], rejets, promotion)

	propositions.remove(p_2)

	return p_2[0], p_2[1]

def huang_kavitha(candidats, formations):
	t = [[0] * len(formations), [0]* len(formations)] 

	r = []
	for k in range(len(formations)):
		r.append(set())

	prop_acceptee = [[0]* len(formations),[0]*len(formations)]

	promotion = [0] * len(formations)

	propositions = []
	for k in range(len(candidats)):
		propositions.append([])

	#M = [{},{}]

	f = formations[0]
	i = 0

	while prop_acceptee[i][f.id] < f.nb_places and promotion[f.id] < 3:
		c = f.candidatures[t[i][f.id]]
		#print("=======")
		#print("Proposition", i, "de formation", f.id, "à candidat", c.id)

		p = propositions[c.id]
		p.append((f, i))
		#print("Tableau des propositions :", propositions)
		prop_acceptee[i][f.id] += 1
		if len(propositions[c.id]) <= 2:
			#print("Candidat", c.id, "a moins de 3 propositions, il accepte")
			#M[i][c] = f
			#nb_prop_acceptees[f.id] += 1
			if prop_acceptee[i][f.id] < f.nb_places:
				t[i][f.id]+=1
		else:
			#print("Candidat",c.id, "a 3 propositions :", propositions[c.id])
			f_r, j = rejette_moins_desirable(c, propositions[c.id], r, promotion)
			#print("Candidat", c.id, "rejette la proposition", j, "de ", f_r.id)

			#nb_prop_acceptees[f_r.id] -= 1
			prop_acceptee[j][f_r.id] -= 1

			if t[j][f_r.id] == len(f_r.candidatures)-1:
				#print("Formation",f_r.id,"arrivé au bout de sa liste")
				t[j][f_r.id] = 0
				while (f_r,j) in propositions[f_r.candidatures[t[j][f_r.id]].id] and t[j][f_r.id] < len(f_r.candidatures) -1:
					t[j][f_r.id] += 1
				if promotion[f_r.id] < 2:
					promotion[f_r.id] += 1
					#print("Formation", f_r.id, "est promue (",promotion[f_r.id],")")
					r[f_r.id] = set()
				else:
					promotion[f_r.id] = 3
					#print("Formation", f_r.id, "a abandonné")
			else:
				t[j][f_r.id] += 1
			#print("Formation", f_r.id, "rejettée")
			r[f_r.id].add(c)
		for f_p in formations:
			if prop_acceptee[0][f_p.id] < f_p.nb_places and t[0][f_p.id] < len(f_p.candidatures) and promotion[f_p.id] < 3:
				i = 0
				f = f_p
				break
			elif prop_acceptee[1][f_p.id] < f_p.nb_places and t[1][f_p.id] < len(f_p.candidatures) and promotion[f_p.id] < 3:
				i = 1
				f = f_p
				break
		#print("Prochaine formation choisie : ", f)
		#print("Taille de sa liste : ", len(f.candidatures))
		#print("Position du prochain candidat appellé : ", t[i][f.id])
		if t[i][f_p.id] == len(f_p.candidatures):
			break
	#for f_p in formations:
		#print("====")
		#print(f_p)
		#print(prop_acceptee[0][f_p.id])
		#print(prop_acceptee[1][f_p.id])

	noeuds, source, puits = creer_graphe_flots(propositions, candidats, formations)

	graphe_flots_max = ford_fulkerson(noeuds, source, puits)

	return affectation_finale(graphe_flots_max, candidats, formations)

def affectation_finale(graphe, candidats, formations):
	M = [None] * len(candidats)

	for i in range(len(formations)):
		for arc in graphe[i+1]:
			if arc.flot == 1:
				M[arc.dest - len(formations) - 1] = i

	return M


def ford_fulkerson(graphe, source, puits):

	graphe_residuel = deepcopy(graphe)

	parent = [0 for i in range(len(graphe_residuel))]

	flot_total = 0
	sys.setrecursionlimit(2000)

	while parcours_profondeur(graphe_residuel, source, [False for i in range(len(graphe_residuel))], puits, parent):
		path = chemin(parent, puits, source)
		c_f = sys.maxsize
		i = 0
		while i < len(path) - 1:
			a = arc_dest(graphe_residuel, path[i], path[i+1])
			if a.capacite < c_f:
				c_f = a.capacite
			i += 1
		#print(c_f)
		flot_total += c_f
		for i in range(len(path)-1):
			n_source = path[i]
			#print(n_source, "->", path[i+1])
			if path[i] < path[i+1]:
				arc = arc_dest(graphe, path[i], path[i+1])
				arc_r = arc_dest(graphe_residuel, path[i], path[i+1])

				arc.flot += c_f
				arc_r.capacite -= c_f
				reverse_arc = arc_dest(graphe_residuel, path[i+1], path[i])
				if reverse_arc != None:
					reverse_arc.capacite += c_f
				else:
					graphe_residuel[path[i+1]].append(Arc(path[i], 0, c_f))
			else:
				arc = arc_dest(graphe, path[i+1], path[i])
				arc_r = arc_dest(graphe_residuel, path[i], path[i+1])

				arc.flot -= c_f
				arc_r.capacite -= c_f
				reverse_arc = arc_dest(graphe_residuel, path[i+1], path[i])
				if reverse_arc != None:
					reverse_arc.capacite += c_f
				else:
					graphe_residuel[path[i]].append(Arc(path[i+1], 0, c_f))

	print("Nb d'affectés avec Huang et Kavitha : ", flot_total)

	#print(graphe)

	return graphe

def arc_dest(graphe, source, dest):
	arc = None
	for a in graphe[source]:
		if a.dest == dest:
			arc = a
			break

	return arc


def chemin(parent, puits, source):
	i = puits
	ch = []
	while i != source:
		ch.insert(0,i)
		i = parent[i]
	ch.insert(0,source)

	return ch

def parcours_profondeur(noeuds, n, visite, puits, parent):
	visite[n] = True
	if n == puits:
		return True

	for a in noeuds[n]:
		if not visite[a.dest] and a.capacite > a.flot:
			#print(n, "--->",a.dest, "(",a.flot,"/",a.capacite,")")
			parent[a.dest] = n
			if parcours_profondeur(noeuds, a.dest, visite, puits, parent):
				return True

	return False

def creer_graphe_flots(propositions, candidats, formations):

	source = 0
	puits = len(formations) + len(candidats) + 1

	noeuds = []
	for k in range(len(candidats) + len(formations) + 2):
		noeuds.append([])

	noeuds[source] = [Arc(i+1, 0, formations[i].nb_places) for i in range(len(formations))]
	noeuds[puits] = []

	for i in range(len(candidats)):
		noeuds[i+1+len(formations)] = [Arc(puits,0,1)]

	for i in range(len(propositions)):
		l = []
		for prop in propositions[i]:
			if prop[0].id not in l:
				l.append(prop[0].id)
				noeuds[prop[0].id+1].append(Arc(i+1+len(formations), 0, 1))

	#print(noeuds)

	return noeuds, source, puits

def test():
	#candidats, formations = ig.generate_instance(20,500)
	candidats, formations = ig.exemple_rapport()
	huang_kavitha(candidats, formations)