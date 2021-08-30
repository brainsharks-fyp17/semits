comp = open("complex-1000.txt").readlines()
simp1 = open("simp1000-piyumika2.txt").readlines()
simp2 = open("simp1000- indumini4.txt").readlines()
assert len(comp) == len(simp1) == len(simp2)
test_data = open("./parallel/si-cc/test.txt", "w")
for i in range(len(comp)):
    test_data.write(comp[i].strip() + " | " + simp1[i].strip() + "\n")
    test_data.write(comp[i].strip() + " | " + simp2[i].strip() + "\n")
test_data.close()
