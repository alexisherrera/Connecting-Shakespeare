from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import networkx as nx
import urllib
import re

r = urllib.urlopen('http://shakespeare.mit.edu/othello/full.html').read()
soup = BeautifulSoup(r)

#create our graph
G=nx.Graph()

#arrays/dictionaries to hold our characters
characters_in_play = {}
characters_in_scene = []
total_characters_list = []

# array with links to all the scenes in the play
scene_links = ['http://shakespeare.mit.edu/othello/othello.1.1.html', 'http://shakespeare.mit.edu/othello/othello.1.2.html', 'http://shakespeare.mit.edu/othello/othello.1.3.html',
'http://shakespeare.mit.edu/othello/othello.2.1.html', 'http://shakespeare.mit.edu/othello/othello.2.2.html', 'http://shakespeare.mit.edu/othello/othello.2.3.html',
'http://shakespeare.mit.edu/othello/othello.3.1.html', 'http://shakespeare.mit.edu/othello/othello.3.2.html', 'http://shakespeare.mit.edu/othello/othello.3.3.html',
'http://shakespeare.mit.edu/othello/othello.3.4.html', 'http://shakespeare.mit.edu/othello/othello.4.1.html', 'http://shakespeare.mit.edu/othello/othello.4.2.html',
'http://shakespeare.mit.edu/othello/othello.4.3.html', 'http://shakespeare.mit.edu/othello/othello.5.1.html', 'http://shakespeare.mit.edu/othello/othello.5.2.html']
#store all a tages in array
temp_arr = soup.find_all("a", {"name": re.compile("speech")})

#get all of the characters and put in play
for element in temp_arr:
    if not element.getText() in characters_in_play:
        characters_in_play[element.getText()] = 0
        total_characters_list.append(element.getText())
        #also add the character to our graph
        G.add_node(element.getText(), label = element.getText())


count = 0

#go scene by scene and update our dictionaries and graphs
for scene in scene_links:
    #get all the characters for a particular scene
    inner_soup = BeautifulSoup(urllib.urlopen(scene).read())
    temp_arr = inner_soup.find_all("a", {"name": re.compile("speech")})
    for element in temp_arr:
        if not element.getText() in characters_in_scene:
            characters_in_scene.append(element.getText())

    #now we wan to update their dictionary values
    for element in temp_arr:
        characters_in_play[element.getText()] = characters_in_play[element.getText()] + 1;

        for character in characters_in_scene:
            if character == element.getText():
                continue
            if G.has_edge(element.getText(), character):
                G[element.getText()][character]['weight'] += 1
            else:
                G.add_edge(element.getText(), character, weight=1)

    count = count + 1
    temp_arr = []
    characters_in_scene = []

#get number of edges
print('------------------------------------')
print("number of edges:")
print(G.number_of_edges())
print('------------------------------------')

#calculate degree of each node
degree_dictionary = G.degree(G.nodes())
for key, value in degree_dictionary.iteritems():
    print(key)
    print('degree:')
    print(value)

print('------------------------------------')

#calculate the degree centrality for each number_of_edges
centrality_dictionary = nx.degree_centrality(G)
for key, value in centrality_dictionary.iteritems():
    print(key)
    print('degree centrality:')
    print(value)
print('------------------------------------')
#calculate the clustering coefficient for each node
clustering_co_dictionary = nx.clustering(G)
for key, value in centrality_dictionary.iteritems():
    print(key)
    print('clustering coefficient:')
    print(value)

pos = nx.circular_layout(G, scale=.5)
nx.draw(G, pos, node_color= 'blue')
edge_labels = nx.get_edge_attributes(G,'r')
edge_labels=nx.draw_networkx_edge_labels(G,pos, edge_labels = edge_labels)
nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif', font_color='red')

plt.axis('off')
plt.show()
