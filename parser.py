import rdflib

alive_g = rdflib.Graph()
g = rdflib.Graph()

# parse in an RDF file
f_name = "graph.ttl"
result = alive_g.parse(f_name, format='turtle')

# to keep track of alive objects
alive_object_list = []

# loop through each triple in the graph (subj, pred, obj)
for subj, pred, obj in alive_g:
    g.add((subj, pred, obj))
    alive_g.remove((subj, pred, obj))

added = True
while(added):
    added = False
    for subj, pred, obj in g:
        # assumption: BNode's are the only empty ones initially
        # later if a BNode was included in a triple, it doesn't count as empty
        if((str(type(subj)) != "<class 'rdflib.term.BNode'>") or
                (subj in alive_object_list)):
            alive_g.add((subj, pred, obj))
            g.remove((subj, pred, obj))
            alive_object_list.append(obj)
            added = True


# print the number of "triples" in the Graph
print("graph has {} statements.".format(len(alive_g)))


with open("alive_" + f_name, 'w') as f:
	# write the entire Graph in the RDF Turtle format to a new file
    f.write(alive_g.serialize(format="turtle").decode("utf-8"))
