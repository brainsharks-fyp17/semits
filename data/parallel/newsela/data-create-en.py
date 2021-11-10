tr_comp = open("/home/rumesh/Downloads/FYP/datasets/newsela-en/train.complex").readlines()
tr_simp = open("/home/rumesh/Downloads/FYP/datasets/newsela-en/train.simple").readlines()
val_comp = open("/home/rumesh/Downloads/FYP/datasets/newsela-en/valid.complex").readlines()
val_simp = open("/home/rumesh/Downloads/FYP/datasets/newsela-en/valid.simple").readlines()

assert len(tr_simp) == len(tr_comp)
assert len(val_simp) == len(val_simp)
train = open("train0.txt", "w")
test = open("test.txt", "w")
dev = open("dev.txt", "w")

for i in range(len(tr_comp)):
    if i < 2000:
        dev.write(tr_comp[i].strip() + " | " + tr_simp[i])
    else:
        train.write(tr_comp[i].strip() + " | " + tr_simp[i])

for i in range(len(val_comp)):
    test.write(val_comp[i].strip() + " | " + val_simp[i])
