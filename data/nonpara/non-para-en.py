comp = open("/home/rumesh/Downloads/FYP/datasets/tsdata/fkdifficpart-2m-1.lower").readlines()
simp = open("/home/rumesh/Downloads/FYP/datasets/tsdata/fkeasypart-2m-1.lower").readlines()

s_tr = open("simp_train.txt", "w")
c_tr = open("comp_train.txt", "w")

s_dv = open("simp_dev.txt", "w")
c_dv = open("comp_dev.txt", "w")

for i in range(len(comp)):
    if i < 2000:
        c_dv.write(comp[i])
    else:
        c_tr.write(comp[i])

for i in range(len(simp)):
    if i < 2000:
        s_dv.write(simp[i])
    else:
        s_tr.write(simp[i])
