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

#Generate a binary vector of length equal to the number of hyperedges
def generate_colors(color_num, m):
	S = [int(char)for char in str(bin(color_num))[2:]]
	T = S + ([0]*(m-len(S))) if len(S) < m else S[:m]
	return T

#Create a dictionary that map each hyperedge to a tuple:(color, index) where color is the color of the hyperedge and index is the index of the hyperedge in lexicographical ordering of the hyperedges
def color_hypergraph(hyperedges, colors):
	col = dict((hyperedges[i],(colors[i],i)) for i in xrange(len(hyperedges)))	
	return col


def generate_coloring_of_hypergraph(color_num,vertex_num):
	edge_set = list(itertools.combinations(range(1,vertex_num+1),4))
	colors = generate_colors(color_num,len(edge_set))
	coloring_map = color_hypergraph(edge_set, colors)
	num_of_red =colors.count(1)
	return coloring_map, num_of_red
	
#Given the coloring map and fixed vertex set, generate a blue and red dictionary where the keys are the pairs of elements of the vertex set and values are the blue/red hyperedges containing that pair
def generate_bipartite_matching(n, vertex_set, color_map):
  red_matching = {}
  blue_matching = {}
  edge_sets =  list(itertools.combinations(vertex_set,2))
  for i in xrange(len(edge_sets)):
	edge_pair_tuple = edge_sets[i]
	edge_pair = set(edge_pair_tuple)
	hyperedges = [tuple(edge_pair.union(add_pair)) for add_pair in itertools.combinations(set(range(1,n+1)).difference(edge_pair),2)]
	for h in hyperedges:
	  (color, j) = color_map[h]
	  if color: #Red is 1, blue is 0
		red_matching.setdefault(edge_pair_tuple, set([])).add(j)
	  else:
		blue_matching.setdefault(edge_pair_tuple, set([])).add(j)
  return red_matching, blue_matching	

#Check if there is perfect matching between all pair of elements in the vertex set to the set of hyperedges containing them.
def check_perfect_matching(n, vertex_set, check_red, check_blue, coloring_map):
  red_matching, blue_matching = generate_bipartite_matching(n, vertex_set, coloring_map)
  cliq_num = len(vertex_set)
  s = cliq_num * (cliq_num-1) /2
  if check_red:
	ns = len(bipartiteMatch(red_matching)[0])
	if (ns >= s): return True
  if check_blue:
	ns = len(bipartiteMatch(blue_matching)[0])
	if (ns >= s): return True
  #Basically means there is no Berge clique
  return False


def contains_berge_graph(n, coloring_map, clique_num, check_red,check_blue):
	for cliques in itertools.combinations(range(1,n+1),clique_num):
	  if check_perfect_matching(n,list(cliques), check_red, check_blue, coloring_map):
		return True
	return False


  
def check_berge(color_num, n, clique_num):
	hyperedge_num = n*(n-1)*(n-2)*(n-3)/24
	#Enough to check half of the coloring since red and blue are symmetric 
	color_max = 2 ** hyperedge_num / 2 + 1 
	min_edge = clique_num * (clique_num-1)/2	
	
	coloring_map, num_of_red= generate_coloring_of_hypergraph(color_num, n)
	num_of_blue = hyperedge_num- num_of_red	
		
	check_red = (num_of_red >= min_edge)
	check_blue= (num_of_blue>= min_edge)
	hasBerge = contains_berge_graph(n, coloring_map, clique_num, check_red, check_blue)
	return hasBerge


@contextmanager
def poolcontext(*args,**kwargs):
  pool = mp.Pool(*args, **kwargs)
  yield pool
  pool.close()
  pool.join()

def num_color(n):
  hyperedge_num = n*(n-1)*(n-2)*(n-3)/24
  color_max = 2 ** hyperedge_num / 2 + 1  
  return color_max

def test(n,clique_num,start_color=0, end_color=None):
  color_max =  num_color(n) if not end_color else end_color
  start = time.time()
  start_date = time.ctime()
  f = open('Ramsey_log.txt','w+')
  f.write("Starting: %s\n" % start_date)
  f.close()
 
  chunk_size = 2**10
  front = start_color
  num_iters = 0
  while front <= color_max:
	colors = range(front, min(front+chunk_size+1,color_max))
	front = front + chunk_size + 1
	num_iters += chunk_size
	with poolcontext(processes = mp.cpu_count()) as pool:
	  results = set(pool.map(partial(check_berge, n=n,clique_num=clique_num), colors))
	if False in results:
	  f = open('Ramsey_log.txt','a+')
	  f.write("NO BLUE OR RED\n")
          f.write("Bad coloring is %d\n" % front)
	  f.close()
	  return
	else: 
	  curr_time = time.time()
	  f = open('Ramsey_log.txt','a+')
          f.write("Starting color: %d, Avg: %f: Progress %d Percentage\n" % (front, ((curr_time-start)/num_iters*10000),(num_iters * 100/(color_max -start_color)))) 
	  f.close()

#Arguments:
  #1:number of vertices in the hypergraph
  #2:number of vertices of the forbidden clique
  #OPTIONAL 3:starting test point
  #OPTIONAL 4: ending test point
test(7,6)

