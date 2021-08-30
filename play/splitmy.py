lines = open("preds").readlines()
ref = open("ref.txt", "w")
pred = open("pre.txt", "w")
ori = open("ori.txt","w")
for line in lines:
    if "Predicted" in line:
        pred.write(line.split("Predicted: ")[1])
    elif "Reference" in line:
        ref.write(line.split("Reference: ")[1])
    elif "Original" in line:
        ori.write(line.split("Original: ")[1])

