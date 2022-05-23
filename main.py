import gale_shapley as gs
import instance_generation as ig
import huang_kavitha as hk
import os
import time

def creer_fichiers(nb_formations = 100, nb_candidats = 10000, nb_voeux_moy = 8, p_ties = 0.05, nb_instances = 1, directory = "instances"):
	return ig.generate_instance(nb_formations, nb_candidats, nb_voeux_moy, p_ties, nb_instances, directory)

def test_instance(fichier, nb):

	if nb == 1:
		candidats, formations = ig.parser_fichier(fichier)
		start_time = time.time()
		x = gs.gale_shapley(candidats,formations)
		t = time.time() - start_time
		#print(t, "secondes")
		return x
	elif nb == 2:
		candidats, formations = ig.parser_fichier(fichier)
		start_time = time.time()
		gs.gale_shapley_plus_pop(candidats,formations)
		t = time.time() - start_time
		print(t, "secondes")
	elif nb == 3:
		candidats, formations = ig.parser_fichier(fichier)
		start_time = time.time()
		gs.gale_shapley_moins_pop(candidats,formations)
		t = time.time() - start_time
		print(t, "secondes")
	elif nb == 4:
		candidats, formations = ig.parser_fichier(fichier)
		start_time = time.time()
		hk.huang_kavitha(candidats,formations)
		t = time.time() - start_time
		print(t, "secondes")
	elif nb == 5:
		candidats, formations = ig.parser_fichier(fichier)
		start_time = time.time()
		gs.gale_shapley_remplissage(candidats,formations)
		t = time.time() - start_time
		print(t, "secondes")

def test_satis(fichier):
	candidats, formations = ig.parser_fichier(fichier)
	M_hk = hk.huang_kavitha(candidats, formations)

	candidats, formations = ig.parser_fichier(fichier)

	M_gs_a = gs.gale_shapley_moins_pop(candidats, formations)

	#print(M_gs_a)

	candidats, formations = ig.parser_fichier(fichier)

	rang_1 = [0] * len(candidats)
	rang_2 = [0] * len(candidats)
	for i in range(len(candidats)):
		rang_1[i] = len(candidats[i].voeux)+1
		rang_2[i] = len(candidats[i].voeux)+1
		for (f,r) in candidats[i].voeux:
			if f.id == M_hk[i]:
				rang_1[i] = r
			if i in M_gs_a and f.id == M_gs_a[i].id:
				rang_2[i] = r
		#print(rang_1[i], rang_2[i])

	cpt_m_sat = 0
	cpt_p_sat = 0
	for i in range(len(candidats)):
		if rang_1[i] < rang_2[i]:
			cpt_p_sat += 1
		elif rang_1[i] > rang_2[i]:
			cpt_m_sat += 1
	print("Candidats moins satisfaits :", cpt_m_sat)
	print("Candidats plus satisfaits :", cpt_p_sat)
"""
for inst in sorted(os.listdir("instances/exp_nb_voeux")):
	print("===============================")
	print(inst)
	print("===============================")
	fichier = "instances/exp_nb_voeux/" + inst
	cpt = 0
	for i in range(10):
		cpt += test_instance(fichier, 1)

	print("Nb d'affectés avec Gale-Shapley (choix aléatoire) :", cpt/10)
	test_instance(fichier, 2)
	test_instance(fichier, 3)
	test_instance(fichier, 5)
	#test_instance(fichier, 4)
"""

c,f = ig.parser_fichier("instances/50_5000_10_3.txt")
gs.gale_shapley_remplissage(c,f)

#c,f = ig.parser_fichier("instances/exemple_rapport.txt")
#print(gs.gale_shapley_remplissage(c,f))

#test_satis("instances/test/test.txt")

"""
for inst in sorted(os.listdir("instances/test")):
	print("===============================")
	print(inst)
	print("===============================")
	fichier = "instances/test/" + inst
	test_satis(fichier)
"""



#creer_fichiers(nb_formations = 50, nb_candidats = 5000, nb_voeux_moy = 6, p_ties = 0.05, nb_instances = 5)
#creer_fichiers(nb_formations = 50, nb_candidats = 5000, nb_voeux_moy = 6, p_ties = 0.1, nb_instances = 5)
#creer_fichiers(nb_formations = 50, nb_candidats = 5000, nb_voeux_moy = 6, p_ties = 0.2, nb_instances = 5)
#creer_fichiers(nb_formations = 100, nb_candidats = 10000, nb_voeux_moy = 8, p_ties = 0.05, nb_instances = 5)
#creer_fichiers(nb_formations = 100, nb_candidats = 10000, nb_voeux_moy = 8, p_ties = 0.1, nb_instances = 5)
#creer_fichiers(nb_formations = 100, nb_candidats = 10000, nb_voeux_moy = 8, p_ties = 0.2, nb_instances = 5)
#creer_fichiers(nb_formations = 250, nb_candidats = 25000, nb_voeux_moy = 10, p_ties = 0.05, nb_instances = 5)
#creer_fichiers(nb_formations = 250, nb_candidats = 25000, nb_voeux_moy = 10, p_ties = 0.1, nb_instances = 5)
#creer_fichiers(nb_formations = 250, nb_candidats = 25000, nb_voeux_moy = 10, p_ties = 0.2, nb_instances = 5)
#creer_fichiers(nb_formations = 500, nb_candidats = 50000, nb_voeux_moy = 12, p_ties = 0.05, nb_instances = 5)
#creer_fichiers(nb_formations = 500, nb_candidats = 50000, nb_voeux_moy = 12, p_ties = 0.1, nb_instances = 5)
#creer_fichiers(nb_formations = 500, nb_candidats = 50000, nb_voeux_moy = 12, p_ties = 0.2, nb_instances = 5)

"""
# test p_ties
creer_fichiers(nb_formations = 1000, nb_candidats = 100000, nb_voeux_moy = 12, p_ties = 0.05, nb_instances = 3, directory="instances/exp_proba_ties")
creer_fichiers(nb_formations = 1000, nb_candidats = 100000, nb_voeux_moy = 12, p_ties = 0.1, nb_instances = 3, directory="instances/exp_proba_ties")
creer_fichiers(nb_formations = 1000, nb_candidats = 100000, nb_voeux_moy = 12, p_ties = 0.2, nb_instances = 3, directory="instances/exp_proba_ties")
creer_fichiers(nb_formations = 1000, nb_candidats = 100000, nb_voeux_moy = 12, p_ties = 0.4, nb_instances = 3, directory="instances/exp_proba_ties")
creer_fichiers(nb_formations = 1000, nb_candidats = 100000, nb_voeux_moy = 12, p_ties = 0.8, nb_instances = 3, directory="instances/exp_proba_ties")
"""
# test nb_voeux_moy
"""creer_fichiers(nb_formations = 1000, nb_candidats = 100000, nb_voeux_moy = 6, p_ties = 0.1, nb_instances = 3, directory="instances/exp_nb_voeux")
creer_fichiers(nb_formations = 1000, nb_candidats = 100000, nb_voeux_moy = 9, p_ties = 0.1, nb_instances = 3, directory="instances/exp_nb_voeux")
creer_fichiers(nb_formations = 1000, nb_candidats = 100000, nb_voeux_moy = 12, p_ties = 0.1, nb_instances = 3, directory="instances/exp_nb_voeux")
creer_fichiers(nb_formations = 1000, nb_candidats = 100000, nb_voeux_moy = 15, p_ties = 0.1, nb_instances = 3, directory="instances/exp_nb_voeux")
creer_fichiers(nb_formations = 1000, nb_candidats = 100000, nb_voeux_moy = 18, p_ties = 0.1, nb_instances = 3, directory="instances/exp_nb_voeux")"""


#creer_fichiers(nb_formations=10, nb_candidats=20, nb_voeux_moy = 2, p_ties = 0.2, nb_instances = 10, directory="instances/test")

#creer_fichiers(nb_formations = 1000, nb_candidats = 100000, nb_voeux_moy=12, p_ties = 0.1, nb_instances = 5)

"""SM (Psup) vs Sm_opt

% remplissage (25,50,75)
nbr d'envois des hopitaux
nbr d'affectéation définitive des élèves (basé sur SM opt)"""