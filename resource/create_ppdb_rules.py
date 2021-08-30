ppdb_lines = open("ppdb-si.txt").readlines()
rules = []
# comp-> simp rules
comp_file = open("./denoise/comp_rules.txt", "w")
for line in ppdb_lines:
    if len(line) > 3 and "-" not in line and "," in line:
        rules.append(line)
        comp_file.write(line)
comp_file.close()
# simp->comp rules
simp_file = open("./denoise/simp_rules.txt", "w")
for rule in rules:
    rule = rule.split(",")
    comp = rule[0].strip()
    simp = rule[1].strip()
    simp_file.write(simp + "," + comp + "\n")
simp_file.close()
