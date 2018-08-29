#Author: Zhiyu Wang
#Email: zhiyuw@math.sc.edu
#Date: 07/24/2018

import itertools
from util2 import *
import multiprocessing as mp
from functools import partial
from contextlib import contextmanager
import sys,os
import time


#c: the integer whose binary representation (with length m) gives us the coloring of the hyperedges where 1 means red and 0 means blue
#m: number of hyperedges
def generate_colors(c, m):
  S = [int(char)for char in str(bin(c))[2:]]
  T = S + ([0]*(m-len(S))) if len(S) < m else S[:m]
  return T

def color_hypergraph(hyperedges, colors):
  col = dict((hyperedges[i],(colors[i],i)) for i in xrange(len(hyperedges)))
  return col

def generate_coloring_of_hypergraph(c,n):
  edge_set = list(itertools.combinations(range(1,n+1),3))
  colors = generate_colors(c,len(edge_set))
  coloring_map = color_hypergraph(edge_set, colors)
  num_of_red =colors.count(1)
  return coloring_map, num_of_red
	

def generate_bipartite_matching(n, vertex_set, color_map):
  red_matching = {}
  blue_matching = {}
  edge_sets =  list(itertools.combinations(vertex_set,2))
  for i in xrange(len(edge_sets)):
	edge_pair_tuple = edge_sets[i]
	edge_pair = set(edge_pair_tuple)

	#Generate all 3-uniform hyperedges containing edge_pair
	hyperedges = [tuple(edge_pair.union(set([elem]))) for elem in set(range(1,n+1)).difference(edge_pair)]
	
	for h in hyperedges:
	  #color: color of the hyperedge
	  #j: index (unique identifier) of the hyperedge
	  (color, j) = color_map[h]
	  if color: # 1 means red
		red_matching.setdefault(edge_pair_tuple, set([])).add(j)
	  else:
		blue_matching.setdefault(edge_pair_tuple, set([])).add(j)
  
  return red_matching, blue_matching	

def check_perfect_matching(n, vertex_set, coloring_map, color):
  red_matching, blue_matching = generate_bipartite_matching(n,vertex_set, coloring_map)
  matching = red_matching if color else blue_matching
  cliq_num = len(vertex_set)
  s = cliq_num * (cliq_num-1)/2
  ns = len(bipartiteMatch(matching)[0])
  return (ns>=s)

def contains_berge_graph(n, coloring_map, blue_clique, red_clique, check_blue, check_red):
	if check_red:
	  for cliques in itertools.combinations(range(1,n+1),red_clique):
		if check_perfect_matching(n,list(cliques), coloring_map, 1):
		  return True
	if check_blue:
	  for cliques in itertools.combinations(range(1,n+1),blue_clique):
		if check_perfect_matching(n,list(cliques), coloring_map, 0):
		  return True			
	return False


def num_color(n):
  hyperedge_num = n*(n-1)*(n-2)/6
  color_max = 2 ** hyperedge_num + 1 
  return color_max

#c: the coloring that we want to test
#n: number of vertices of the complete 3-uniform host graph
#blue: order of the forbidden blue clique
#red:  order of the forbidden red clique
def check_berge(c, n, blue_clique, red_clique):
	hyperedge_num = n*(n-1)*(n-2)/6
	color_max = num_color(n) 
	blue_min_edge = blue_clique * (blue_clique-1)/2	
	red_min_edge = red_clique * (red_clique-1)/2	
	
	coloring_map, num_of_red= generate_coloring_of_hypergraph(c, n)
	num_of_blue = hyperedge_num- num_of_red	
	
	#if the number of red edges < red_min_edge, no need to check red_clique
	#same to blue
	check_red = (num_of_red >= red_min_edge)
	check_blue= (num_of_blue>= blue_min_edge)

	hasBerge = contains_berge_graph(n, coloring_map, blue_clique, red_clique, \
	check_blue, check_red)
	return hasBerge

#blue_clique: the order of the forbidden blue clique
#red_clique:  the order of the forbidden red  clique
#n: number of vertices of the 3-uniform complete host graph
def test(blue_clique, red_clique, n):
  color_max =  num_color(n)
  start = time.time()
  start_date = time.ctime()
  f = open('Ramsey_log.txt','w+')
  f.write("Starting: %s\n" % start_date)
  f.close()
 
  for c in xrange(color_max):
	if c % 10000 == 0: #For progress tracking only
	  print c
	res = check_berge(c, n, blue_clique, red_clique)
	if not res:
	  print "No Blue or Red"
	  print c
	  return
  print "Success"

test(4,5,6)

