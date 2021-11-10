import pickle

ppdb_ori = "/home/rumesh/Downloads/FYP/datasets/SimplePPDB"
ppdb_ori = open(ppdb_ori).readlines()
comp_file = open("comp_rules.pkl", "wb")
simp_file = open("simp_rules.pkl", "wb")
comp_dict = dict()
simp_dict = dict()
for i in range(len(ppdb_ori)):
    _, prob, _, comp, simp = ppdb_ori[i].strip().split("\t")
    if float(prob) > 0.5:
        if comp in comp_dict:
            comp_dict[comp].append(simp)
        else:
            comp_dict[comp] = [simp]

        if simp in simp_dict:
            simp_dict[simp].append(comp)
        else:
            simp_dict[simp] = [comp]

pickle.dump(comp_dict, comp_file)
pickle.dump(simp_dict, simp_file)
