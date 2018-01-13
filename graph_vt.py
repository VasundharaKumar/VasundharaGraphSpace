from collections import Counter
import os
import json
from graphspace_python.api.client import GraphSpace
import matplotlib.pyplot as plt
import pandas as pd

graphspace = GraphSpace('user1@example.com', 'user1')
public_graphs = graphspace.get_public_graphs(limit=10000)

print "Number of public graphs stored in GraphSpace."
print len(public_graphs)


user_graph_and_count = Counter()

for each_graph in public_graphs:
	user_graph_and_count[str(each_graph.owner_email)] += 1

sorted_by_count_data = sorted(user_graph_and_count, key=user_graph_and_count.get, reverse=True)
for w in sorted_by_count_data:
	print w, user_graph_and_count[w]


no_of_nodes = []
no_of_edges = []

i = 0
current_directory = os.getcwd()
output_directory = os.path.join(current_directory, r'output_folder')
if not os.path.exists(output_directory):
   os.makedirs(output_directory)

for each in public_graphs:
    graph_obj = graphspace.get_graph(graph_id=each.id)
    json_obj = graph_obj.get_graph_json()
    with open(os.path.join(output_directory, str(each.id) + '.json'), 'w') as outfile:
    	json.dump(json_obj, outfile)

    with open(os.path.join(output_directory, str(each.id) + '.json'), 'r') as outfile:
    	json_graph = json.load(outfile)
    	print "Graph ID", each.id
    	if i%10 == 0:
    		print i, " Objects Processed"
    	nodes_len = len(json_graph['elements']['nodes'])
    	edges_len = len(json_graph['elements']['edges'])
    	no_of_nodes.append(nodes_len)
    	no_of_edges.append(edges_len)
    	print "No of Nodes: ", nodes_len
    	print "No of Edges: ", edges_len
    i += 1
# print no_of_nodes
# print no_of_edges


plt.hist(no_of_nodes)
plt.title("Nodes Histogram")
fig = plt.gcf()
fig.savefig(os.path.join(output_directory, 'nodes1.png'))

print "Generated nodes Histogram"

plt.hist(no_of_edges)
plt.title("Edges Histogram")
fig = plt.gcf()

fig.savefig(os.path.join(output_directory,'edges1.png'))

print "Generated edges Histogram"



df = pd.DataFrame(user_graph_and_count, index=[0])
df = df.transpose()
df = df.reset_index()
df.columns = ['Email', 'Graph Count']
df = df.sort_values('Graph Count', ascending=False)

df.set_index('Email', inplace=True)
table_html = df.to_html().replace('\n', '')

final_html = "<html><body>" + table_html + "<br/><img src='nodes1.png'/><br/><br/><img src='edges1.png'/></body></html>" 

with open(os.path.join(output_directory,'output.html'), 'w') as outfile:
    outfile.write(final_html)

