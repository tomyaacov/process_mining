alphabet = [str(p)+str(r)+str(c) for p in ["A", "B"] for r in range(6) for c in range(7)]

partitions = {
"player": dict([(x,x[0]) for x in alphabet])
}

for r in range(6):
    for c in range(7):
        d = dict([(x,x[1:] if x[1:] == str(r)+str(c) else "-") for x in alphabet])
        partitions["cell" + str(r)+str(c)] = d

for c in range(7):
    d = dict([(x,x[1:] if x[2] == str(c) else "-") for x in alphabet])
    partitions["column" +str(c)] = d

for r in range(6):
    for c in range(7-4+1):
        for p in ["A", "B"]:
            row = [str(p)+str(r)+str(c+i) for i in range(4)]
            d = dict([(x, ",".join(row) if x in row else "-") for x in alphabet])
            partitions["row-" + ",".join(row)] = d

for c in range(7):
    for r in range(6-4+1):
        for p in ["A", "B"]:
            row = [str(p)+str(r+i)+str(c) for i in range(4)]
            d = dict([(x, ",".join(row) if x in row else "-") for x in alphabet])
            partitions["row-" + ",".join(row)] = d

for r in range(6-4+1):
    for c in range(7-4+1):
        for p in ["A", "B"]:
            row = [str(p)+str(r + i) + str(c+i) for i in range(4)]
            d = dict([(x, ",".join(row) if x in row else "-") for x in alphabet])
            partitions["row-" + ",".join(row)] = d

for r in range(6-4+1):
    for c in range(7-4+1):


partitions = {
    "player": lambda x: x[0],
    "cell0": lambda x: x[1] if x[1] == str(0) else "-",
    "cell1": lambda x: x[1] if x[1] == str(1) else "-",
    "cell2": lambda x: x[1] if x[1] == str(2) else "-",
    "cell3": lambda x: x[1] if x[1] == str(3) else "-",
    "cell4": lambda x: x[1] if x[1] == str(4) else "-",
    "cell5": lambda x: x[1] if x[1] == str(5) else "-",
    "cell6": lambda x: x[1] if x[1] == str(6) else "-",
    "cell7": lambda x: x[1] if x[1] == str(7) else "-",
    "cell8": lambda x: x[1] if x[1] == str(8) else "-",
    "row-O0,O1,O2": lambda x: "O0,O1,O2" if x in ['O0', 'O1', 'O2'] else "-",
    "row-X0,X1,X2": lambda x: "X0,X1,X2" if x in ['X0', 'X1', 'X2'] else "-",
    "row-O3,O4,O5": lambda x: "O3,O4,O5" if x in ['O3', 'O4', 'O5'] else "-",
    "row-X3,X4,X5": lambda x: "X3,X4,X5" if x in ['X3', 'X4', 'X5'] else "-",
    "row-O6,O7,O8": lambda x: "O6,O7,O8" if x in ['O6', 'O7', 'O8'] else "-",
    "row-X6,X7,X8": lambda x: "X6,X7,X8" if x in ['X6', 'X7', 'X8'] else "-",
    "row-O0,O3,O6": lambda x: "O0,O3,O6" if x in ['O0', 'O3', 'O6'] else "-",
    "row-X0,X3,X6": lambda x: "X0,X3,X6" if x in ['X0', 'X3', 'X6'] else "-",
    "row-O1,O4,O7": lambda x: "O1,O4,O7" if x in ['O1', 'O4', 'O7'] else "-",
    "row-X1,X4,X7": lambda x: "X1,X4,X7" if x in ['X1', 'X4', 'X7'] else "-",
    "row-O2,O5,O8": lambda x: "O2,O5,O8" if x in ['O2', 'O5', 'O8'] else "-",
    "row-X2,X5,X8": lambda x: "X2,X5,X8" if x in ['X2', 'X5', 'X8'] else "-",
    "row-O0,O4,O8": lambda x: "O0,O4,O8" if x in ['O0', 'O4', 'O8'] else "-",
    "row-X0,X4,X8": lambda x: "X0,X4,X8" if x in ['X0', 'X4', 'X8'] else "-",
    "row-O2,O4,O6": lambda x: "O2,O4,O6" if x in ['O2', 'O4', 'O6'] else "-",
    "row-X2,X4,X6": lambda x: "X2,X4,X6" if x in ['X2', 'X4', 'X6'] else "-"
}

events_map = {
"player":{
    "X": ["X"+str(x) for x in range(9)],
    "O": ["O" + str(x) for x in range(9)]
},
"cell0":{
    "0": ["X0", "O0"],
    "-": ["X"+str(x) for x in range(9) if x!=0] + ["O" + str(x) for x in range(9) if x!=0]
},
"cell1":{
    "1": ["X1", "O1"],
    "-": ["X"+str(x) for x in range(9) if x!=1] + ["O" + str(x) for x in range(9) if x!=1]
},
"cell2":{
    "2": ["X2", "O2"],
    "-": ["X"+str(x) for x in range(9) if x!=2] + ["O" + str(x) for x in range(9) if x!=2]
},
"cell3":{
    "3": ["X3", "O3"],
    "-": ["X"+str(x) for x in range(9) if x!=3] + ["O" + str(x) for x in range(9) if x!=3]
},
"cell4":{
    "4": ["X4", "O4"],
    "-": ["X"+str(x) for x in range(9) if x!=4] + ["O" + str(x) for x in range(9) if x!=4]
},
"cell5":{
    "5": ["X5", "O5"],
    "-": ["X"+str(x) for x in range(9) if x!=5] + ["O" + str(x) for x in range(9) if x!=5]
},
"cell6":{
    "6": ["X6", "O6"],
    "-": ["X"+str(x) for x in range(9) if x!=6] + ["O" + str(x) for x in range(9) if x!=6]
},
"cell7":{
    "7": ["X7", "O7"],
    "-": ["X"+str(x) for x in range(9) if x!=7] + ["O" + str(x) for x in range(9) if x!=7]
},
"cell8":{
    "8": ["X8", "O8"],
    "-": ["X"+str(x) for x in range(9) if x!=8] + ["O" + str(x) for x in range(9) if x!=8]
},
"row-O0,O1,O2":{
    "O0,O1,O2": ['O0', 'O1', 'O2'],
    "-": ["X"+str(x) for x in range(9)] + ["O" + str(x) for x in range(9) if x not in [0,1,2]]
},
"row-X0,X1,X2":{
    "X0,X1,X2": ['X0', 'X1', 'X2'],
    "-": ["X"+str(x) for x in range(9) if x not in [0,1,2]] + ["O" + str(x) for x in range(9)]
},
"row-O3,O4,O5":{
    "O3,O4,O5": ['O3', 'O4', 'O5'],
    "-": ["X"+str(x) for x in range(9)] + ["O" + str(x) for x in range(9) if x not in [3,4,5]]
},
"row-X3,X4,X5":{
    "X3,X4,X5": ['X3', 'X4', 'X5'],
    "-": ["X"+str(x) for x in range(9) if x not in [3,4,5]] + ["O" + str(x) for x in range(9)]
},
"row-O6,O7,O8":{
    "O6,O7,O8": ['O6', 'O7', 'O8'],
    "-": ["X"+str(x) for x in range(9)] + ["O" + str(x) for x in range(9) if x not in [6,7,8]]
},
"row-X6,X7,X8":{
    "X6,X7,X8": ['X6', 'X7', 'X8'],
    "-": ["X"+str(x) for x in range(9) if x not in [6,7,8]] + ["O" + str(x) for x in range(9)]
},
"row-O0,O3,O6":{
    "O0,O3,O6": ['O0', 'O3', 'O6'],
    "-": ["X"+str(x) for x in range(9)] + ["O" + str(x) for x in range(9) if x not in [0,3,6]]
},
"row-X0,X3,X6":{
    "X0,X3,X6": ['X0', 'X3', 'X6'],
    "-": ["X"+str(x) for x in range(9) if x not in [0,3,6]] + ["O" + str(x) for x in range(9)]
},
"row-O1,O4,O7":{
    "O1,O4,O7": ['O1', 'O4', 'O7'],
    "-": ["X"+str(x) for x in range(9)] + ["O" + str(x) for x in range(9) if x not in [1,4,7]]
},
"row-X1,X4,X7":{
    "X1,X4,X7": ['X1', 'X4', 'X7'],
    "-": ["X"+str(x) for x in range(9) if x not in [1,4,7]] + ["O" + str(x) for x in range(9)]
},
"row-O2,O5,O8":{
    "O2,O5,O8": ['O2', 'O5', 'O8'],
    "-": ["X"+str(x) for x in range(9)] + ["O" + str(x) for x in range(9) if x not in [2,5,8]]
},
"row-X2,X5,X8":{
    "X2,X5,X8": ['X2', 'X5', 'X8'],
    "-": ["X"+str(x) for x in range(9) if x not in [2,5,8]] + ["O" + str(x) for x in range(9)]
},
"row-O0,O4,O8":{
    "O0,O4,O8": ['O0', 'O4', 'O8'],
    "-": ["X"+str(x) for x in range(9)] + ["O" + str(x) for x in range(9) if x not in [0,4,8]]
},
"row-X0,X4,X8":{
    "X0,X4,X8": ['X0', 'X4', 'X8'],
    "-": ["X"+str(x) for x in range(9) if x not in [0,4,8]] + ["O" + str(x) for x in range(9)]
},
"row-O2,O4,O6":{
    "O2,O4,O6": ['O2', 'O4', 'O6'],
    "-": ["X"+str(x) for x in range(9)] + ["O" + str(x) for x in range(9) if x not in [2,4,6]]
},
"row-X2,X4,X6":{
    "X2,X4,X6": ['X2', 'X4', 'X6'],
    "-": ["X"+str(x) for x in range(9) if x not in [2,4,6]] + ["O" + str(x) for x in range(9)]
}

}