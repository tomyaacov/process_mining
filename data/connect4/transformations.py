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

# for r in range(6-4+1):
#     for c in range(7-4+1):
#         for p in ["A", "B"]:
#             row = [str(p)+str(r + i) + str(c+i) for i in range(4)]
#             d = dict([(x, ",".join(row) if x in row else "-") for x in alphabet])
#             partitions["row-" + ",".join(row)] = d
#
# for r in range(6-4+1):
#     for c in range(7-4+1):

events_map = {}

for k,v in partitions.items():
    events_map[k] = {}
    for c,t in v.items():
        events_map[k][t] = events_map[k].get(t,[]) + [c]
