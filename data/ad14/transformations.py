partitions = {
    "letter": lambda x: x[0],
    "number": lambda x: x[1],
}

events_map = {
"letter":{
    "A": ["A"+str(x) for x in range(1,5)],
    "B": ["B"+str(x) for x in range(1,5)],
    "C": ["C"+str(x) for x in range(1,5)],
    "D": ["D"+str(x) for x in range(1,5)],
},
"number":{
    "1": [str(x)+"1" for x in "ABCD"],
    "2": [str(x)+"2" for x in "ABCD"],
    "3": [str(x)+"3" for x in "ABCD"],
    "4": [str(x)+"4" for x in "ABCD"],
},
}