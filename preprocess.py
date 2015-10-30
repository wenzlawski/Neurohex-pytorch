import numpy as np
"""
raw_games.dat contains a list of moves corresponding to a 13x13 hex game on each line.
This program converts this into an array of hex positions represented as a 4x17x17
boolean tensor where the 4 channels represent (in order) white, black, west edge connection
and east edge connection. The additional width (17x17 instead of 13x13) is to 
include the edges of the board which are automatically colored for the appropriate
player and edge connected appropriately, additionally this allows a 5x5 input layer 
filter to be placed on directly on the edges without going out of range. Every position 
is transformed to be white-to-play (by reflection and white-black swap of 
black-to-play positions). 
"""
white = 0
black = 1
west = 2
east = 3
boardsize = 13
padding = 2
input_size = boardsize+2*padding
neighbor_patterns = ((-1,0), (0,-1), (-1,1), (0,1), (1,0), (1,-1))

def neighbors(cell):
		"""
		Return list of neighbors of the passed cell.
		"""
		x = cell[0]
		y=cell[1]
		return [(n[0]+x , n[1]+y) for n in neighbor_patterns\
			if (padding<=n[0]+x and n[0]+x<boardsize+padding and padding<=n[1]+y and n[1]+y<boardsize+padding)]

def flood_fill(game, cell, edge):
	game[edge, cell[0], cell[1]] = 1
	for n in neighbors(cell):
		if(game[white, n[0], n[1]] and not game[edge, n[0], n[1]]):
			flood_fill(game, n, edge)


def new_game():
	game = np.zeros((4,input_size,input_size), dtype=bool)
	game[white, 0:padding, :] = 1
	game[white, input_size-padding:, :] = 1
	game[west, 0:padding, :] = 1
	game[east, input_size-padding:, :] = 1
	game[black, :, 0:padding] = 1
	game[black, :, input_size-padding:] = 1
	return game

def play_move(game, move):
	x =	ord(move[0].lower())-ord('a')+padding
	y = int(move[1:])-1+padding
	west_connection = False
	east_connection = False
	game[white, x, y] = 1
	for n in neighbors((x,y)):
		if(game[east, n[0], n[1]]):
			east_connection = True
		if(game[west, n[0], n[1]]):
			west_connection = True
	if(east_connection):
		flood_fill(game, (x,y), east)
	if(west_connection):
		flood_fill(game, (x,y), west)

def preprocess(filename):
	infile = open(filename, 'r')
	positions = []
	for line in infile:
		game = new_game()
		moves = line.split()
		#don't want to add terminal states to initialization positions
		del moves[-1]
		for move in moves:
			play_move(game, move)
			positions.append(np.copy(game))

