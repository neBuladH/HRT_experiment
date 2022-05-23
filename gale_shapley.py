import instance_generation as ig
import random

# voeu : couple (formation, rang)

# les formations à égalité sont ordonnées de façon aléatoire
def gale_shapley(candidats, formations):
	t = [0] * len(formations)
	nb_affectes = [0] * len(formations)
	M = {}
	affectations = 0

	## PREPROCESSING : CASSAGE DES EGALITES

	for c in candidats:
		i = 0
		while i < len(c.voeux):
			tie = [c.voeux[i]]
			j = i+1
			while j < len(c.voeux) and c.voeux[j][1] == c.voeux[i][1]:
				tie.append(c.voeux[j])
				j += 1
			random.shuffle(tie)
			for k in range(len(tie)):
				c.voeux[i+k] = tie[k]

			i = j

		#print(c.voeux)
	##

	f = formations[0]

	while nb_affectes[f.id] < f.nb_places and t[f.id] < len(formations[f.id].candidatures):
		c = f.candidatures[t[f.id]]
		if c.id in M:
			nb_affectes[M[c.id].id] -= 1
		else:
			affectations += 1

		M[c.id] = f
		nb_affectes[f.id] += 1
		t[f.id] += 1


		i = 0
		while c.voeux[i][0] != f:
			i += 1
		j = i+1
		while j < len(c.voeux):
			f_s = c.voeux[j][0]
			f_s.candidatures.remove(c)
			j += 1
		c.voeux = c.voeux[:i]

		for f_p in formations:
			if nb_affectes[f_p.id] < f_p.nb_places and t[f_p.id] < len(formations[f_p.id].candidatures):
				f = f_p
				break

	return affectations

# les formations à égalité sont ordonnées selon leur popularité (les moins populaires sont favorisées)
def gale_shapley_moins_pop(candidats, formations):
	t = [0] * len(formations)
	nb_affectes = [0] * len(formations)
	meme_rang = [None] * len(candidats)
	for i in range(len(meme_rang)):
		meme_rang[i] = []
	M = {}
	affectations = 0

	## PREPROCESSING : CASSAGE DES EGALITES

	for c in candidats:
		i = 0
		while i < len(c.voeux):
			tie = [c.voeux[i]]
			j = i+1
			while j < len(c.voeux) and c.voeux[j][1] == c.voeux[i][1]:
				tie.append(c.voeux[j])
				j += 1
			tie.sort(key=lambda x: x[0].popularite)
			for k in range(len(tie)):
				c.voeux[i+k] = tie[k]

			i = j

		#print(c.voeux)
	##

	f = formations[0]

	while nb_affectes[f.id] < f.nb_places and t[f.id] < len(formations[f.id].candidatures):
		#print("======")
		c = f.candidatures[t[f.id]]
		#print("Proposition de formation", f.id,"à candidat",c.id)
		if c.id in M:
			#print("Candidat",c.id, "déjà affecté à une moins bonne formation :", M[c.id].id)
			nb_affectes[M[c.id].id] -= 1
		else:
			#print("Nouvelle affectation")
			affectations += 1

		M[c.id] = f
		nb_affectes[f.id] += 1
		t[f.id] += 1


		i = 0
		while c.voeux[i][0] != f:
			i += 1
		j = i+1
		while j < len(c.voeux):
			f_s = c.voeux[j][0]
			f_s.candidatures.remove(c)
			j += 1
		c.voeux = c.voeux[:i]

		for f_p in formations:
			if nb_affectes[f_p.id] < f_p.nb_places and t[f_p.id] < len(formations[f_p.id].candidatures):
				f = f_p
				break

	print("Nb d'affectés avec Gale-Shapley (choix du moins populaire) :", affectations)

	return M

# les formations à égalité sont ordonnées selon leur popularité (les plus populaires sont favorisées)
def gale_shapley_plus_pop(candidats, formations):
	t = [0] * len(formations)
	nb_affectes = [0] * len(formations)
	meme_rang = [None] * len(candidats)
	for i in range(len(meme_rang)):
		meme_rang[i] = []
	M = {}
	affectations = 0

	## PREPROCESSING : CASSAGE DES EGALITES

	for c in candidats:
		i = 0
		while i < len(c.voeux):
			tie = [c.voeux[i]]
			j = i+1
			while j < len(c.voeux) and c.voeux[j][1] == c.voeux[i][1]:
				tie.append(c.voeux[j])
				j += 1
			tie.sort(key=lambda x: x[0].popularite, reverse=True)
			for k in range(len(tie)):
				c.voeux[i+k] = tie[k]

			i = j
	##

	f = formations[0]

	while nb_affectes[f.id] < f.nb_places and t[f.id] < len(formations[f.id].candidatures):
		c = f.candidatures[t[f.id]]
		if c.id in M:
			nb_affectes[M[c.id].id] -= 1
		else:
			affectations += 1

		M[c.id] = f
		nb_affectes[f.id] += 1
		t[f.id] += 1


		i = 0
		while c.voeux[i][0] != f:
			i += 1
		j = i+1
		while j < len(c.voeux):
			f_s = c.voeux[j][0]
			f_s.candidatures.remove(c)
			j += 1
		c.voeux = c.voeux[:i]

		for f_p in formations:
			if nb_affectes[f_p.id] < f_p.nb_places and t[f_p.id] < len(formations[f_p.id].candidatures):
				f = f_p
				break

	print("Nb d'affectés avec Gale-Shapley (choix du plus populaire) :", affectations)

	return M

# les formations à égalité sont ordonnées selon leur remplissage courant (les moins remplies sont favorisées)
def gale_shapley_remplissage(candidats, formations):
	t = [0] * len(formations)
	nb_affectes = [0] * len(formations)
	meme_rang = [None] * len(candidats)
	for i in range(len(meme_rang)):
		meme_rang[i] = []
	M = {}
	affectations = 0

	f = formations[0]

	while nb_affectes[f.id] < f.nb_places and t[f.id] < len(formations[f.id].candidatures):
		c = f.candidatures[t[f.id]]

		#print("====")
		#print("Formation ", f.id, " propose à candidat ", c.id)

		if c.id in M:
			#print("Candidat",c.id,"déjà affecté")

			rang_1, rang_2 = get_rangs(c, f, M[c.id])

			if rang_1 == rang_2:
				places_restantes_1 = f.nb_places - nb_affectes[f.id]
				places_restantes_2 = M[c.id].nb_places - nb_affectes[f.id]
				if places_restantes_1 >= places_restantes_2:
					rang_1 -= 1
				else:
					rang_1 += 1
			if rang_1 > rang_2:
				#print("Formation",f.id, "pas assez bonne")
				t[f.id] += 1
			else:
				#print("Formation",f.id, "remplace formation",M[c.id].id)
				nb_affectes[M[c.id].id] -= 1
				nb_affectes[f.id] += 1
				M[c.id] = f
				t[f.id] += 1

		else:
			#print("Première affectation de candidat",c.id)
			nb_affectes[f.id] += 1
			affectations += 1
			M[c.id] = f
			t[f.id] += 1

		for f_p in formations:
			if nb_affectes[f_p.id] < f_p.nb_places and t[f_p.id] < len(formations[f_p.id].candidatures):
				f = f_p
				break

	print("Nb d'affectés avec Gale-Shapley (choix du moins rempli) :", affectations)

	return M

# retourne les rangs respectifs de f_1 et f_2 dans la liste de c
def get_rangs(c, f_1, f_2):
	rang_1 = -1
	rang_2 = -1
	for (f,r) in c.voeux:
		if f == f_1:
			rang_1 = r
		if f == f_2:
			rang_2 = r

	return rang_1, rang_2


def test():
	#candidats, formations = ig.generate_instance()
	candidats, formations = ig.exemple_rapport()
	gale_shapley(candidats, formations)