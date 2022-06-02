import random

bbd = [
"..#*#..",
"...#...",
".......",
".~~.~~.",
".~~.~~.",
".~~.~~.",
".......",
"...#...",
"..#*#.."]

directions = [(0,1),(1,0),(-1,0),(0,-1)]

def tile_type(x,y):
	if bbd[y][x] == '.':
		return 0 #laka
	if bbd[y][x] == '~':
		return 1 #staw
	if bbd[y][x] == '#':
		return 2 #pulapka
	if bbd[y][x] == '*':
		return 3 #jama

def adj(pos1,pos2):
	if pos1[0] == pos2[0]:
		if pos1[1] == pos2[1]-1 or pos1[1] == pos2[1]+1:
			return True
	if pos1[1] == pos2[1]:
		if pos1[0] == pos2[0]-1 or pos1[0] == pos2[0]+1:
			return True
	return False

class board:
	pieces = []
	def __init__(self):
		self.peace = 0
		self.movpl = 0

		self.pieces = []
		self.pieces += [{}]
		self.pieces += [{}]

		self.pieces[0][0] = (0,2)
		self.pieces[0][1] = (5,1)
		self.pieces[0][2] = (1,1)
		self.pieces[0][3] = (4,2)
		self.pieces[0][4] = (2,2)
		self.pieces[0][5] = (6,0)
		self.pieces[0][6] = (0,0)
		self.pieces[0][7] = (6,2)

		self.pieces[1][0] = (6,6)
		self.pieces[1][1] = (1,7)
		self.pieces[1][2] = (5,7)
		self.pieces[1][3] = (2,6)
		self.pieces[1][4] = (4,6)
		self.pieces[1][5] = (0,8)
		self.pieces[1][6] = (6,8)
		self.pieces[1][7] = (0,6)

	def occ(self,x,y):
		for i in range(8):
			if self.pieces[0][i][0] == x and self.pieces[0][i][1] == y:
				return (0,i)
			if self.pieces[1][i][0] == x and self.pieces[1][i][1] == y:
				return (1,i)
		return (-1,-1)

	def pos_move(self,p,dir):
		pos = self.pieces[self.movpl][p]
		if pos[0] == -1:
			return (False,-1,-1)
		t1 = tile_type(pos[0],pos[1])

		posn = (pos[0] + dir[0], pos[1] + dir[1])
		if posn[0] < 7 and posn[0] >= 0 and posn[1] < 9 and posn[1] >= 0:
			t2 = tile_type(posn[0],posn[1])
			pc = self.occ(posn[0],posn[1])
			if (p == 5 or p == 6) and t1 == 0 and t2 == 1: #skok przez wode
				while t2 == 1:
					if pc[0] == 1-self.movpl:
						return (False,-1,-1)
						break #wrogi szczur
					posn = (posn[0] + dir[0],posn[1] + dir[1])
					pc = self.occ(posn[0],posn[1])
					t2 = tile_type(posn[0],posn[1])
				if pc[0] == self.movpl or (pc[0] == 1-self.movpl and pc[1] > p):
					return (False,-1,-1)
				return (True,posn[0],posn[1])
			if p == 0 and t1 == 1 and t2 == 0: #wychodzenie z wody
				if pc[0] == -1:
					return (True,posn[0],posn[1])
				return (False,-1,-1)
			if t2 == 1: #wchodzenie do wody
				if p != 0:
					return (False,-1,-1)
				return (True,posn[0],posn[1])
			if t2 == 3: #wchodzenie do jamy
				if posn[1] == self.movpl*8:
					return (False,-1,-1)
				return (True,posn[0],posn[1])
			if pc[0] != -1: #bicie na ladzie
				if pc[0] == self.movpl: #bicie samego siebie
					return (False,-1,-1)
				if t1 == 2: #bicie z pulapki
					return (False,-1,-1)
				if t2 == 2: #bicie w pulapce
					return (True,posn[0],posn[1])
				if p == 0 and (pc[1] == 7 or pc[1] == 0): #szczur bije
					return (True,posn[0],posn[1])
				if p == 7 and pc[1] != 0: #slon bije
					return (True,posn[0],posn[1])
				if p != 7 and p != 0: #reszta sytuacji
					if p >= pc[1]:
						return (True,posn[0],posn[1])
				return (False,-1,-1)
			return (True,posn[0],posn[1])
		return (False,-1,-1)

	def get_moves(self):
		ret = []
		for i in range(8):
			for d in directions:
				res = self.pos_move(i,d)
				if res[0]:
					ret += [(i,res[1],res[2])]
		return ret

	def apply_move(self,p,x,y):
		self.pieces[self.movpl][p] = (x,y)
		self.movpl = 1 - self.movpl
		self.peace += 1
		for i in range(8):
			if self.pieces[self.movpl][i][0] == x and self.pieces[self.movpl][i][1] == y:
				self.pieces[self.movpl][i] = (-1,-1)
				self.peace = 0
				break
		if tile_type(x,y) == 3:
			return (True,1 - self.movpl)
		if self.peace >= 30:
			for i in range(7,-1,-1):
				if self.pieces[0][i][0] != -1 and self.pieces[1][i][0] == -1:
					return (True,0)
				if self.pieces[1][i][0] != -1 and self.pieces[0][i][0] == -1:
					return (True,1)
			return (True,1)
		return (False,-1)

def cpboard(bd):
	cb = board()
	cb.movpl = bd.movpl
	cb.peace = bd.peace
	for i in range(8):
		cb.pieces[0][i] = (bd.pieces[0][i][0], bd.pieces[0][i][1])
		cb.pieces[1][i] = (bd.pieces[1][i][0], bd.pieces[1][i][1])
	return cb

maks_num = 2000
maks_par = 50

def rand_game(bd,num):
	mv = bd.get_moves()
	if len(mv) == 0:
		return (True,3-bd.movpl,num)
	ri = random.randint(0,len(mv)-1)
	res = bd.apply_move(mv[ri][0],mv[ri][1],mv[ri][2])
	num += 1
	if res[0] == True:
		return (res[0],res[1],num)
	mv = []
	if num >= maks_num:
		return (True,4,num)
	return rand_game(bd,num)

def eval(bd,mov):
	num = 0
	par = 0
	wins = 0.0
	fails = 0.0
	b2 = cpboard(bd)
	res = b2.apply_move(mov[0],mov[1],mov[2])
	if res[0] == True:
		if res[1] != b2.movpl:
			return 1.0
		return 0.0
	while num < maks_num and par < maks_par:
		b3 = cpboard(b2)
		r = rand_game(b3,num)
		num = r[2]
		if r[1] == b2.movpl or r[1] == b2.movpl+2:
			fails += 1.0
		if r[1] == 1-b2.movpl or r[1] == 3-b2.movpl:
			wins += 1.0
		par += 1
	if wins == 0.0:
		return 0.0
	return wins/(wins+fails)

def agent_ran(bd,mv):
	return mv[random.randint(0,len(mv)-1)]

def agent1(bd,mv):
	maksmov = mv[0]
	makscof = 0.0
	for i in mv:
		e = eval(bd,i)
		if e > makscof:
			makscof = e
			maksmov = i
	return maksmov

max_turns = 100000

its1 = {
	0 : 'R',
	1 : 'C',
	2 : 'D',
	3 : 'W',
	4 : 'J',
	5 : 'T',
	6 : 'L',
	7 : 'E'
}

its2 = {
	0 : 'r',
	1 : 'c',
	2 : 'd',
	3 : 'w',
	4 : 'j',
	5 : 't',
	6 : 'l',
	7 : 'e'
}

def visual(bd):
	tmp = [
	"..#*#..",
	"...#...",
	".......",
	".~~.~~.",
	".~~.~~.",
	".~~.~~.",
	".......",
	"...#...",
	"..#*#.."]
	for i in range(8):
		if bd.pieces[0][i][0] != -1:
			tmp[bd.pieces[0][i][1]] = tmp[bd.pieces[0][i][1]][:bd.pieces[0][i][0]] + its1[i] + tmp[bd.pieces[0][i][1]][bd.pieces[0][i][0]+1:]
		if bd.pieces[1][i][0] != -1:
			tmp[bd.pieces[1][i][1]] = tmp[bd.pieces[1][i][1]][:bd.pieces[1][i][0]] + its2[i] + tmp[bd.pieces[1][i][1]][bd.pieces[1][i][0]+1:]
	for i in range(9):
		print(tmp[i])
	print()
	print()

def sim_game(a1):
	bd = board()
	turns = 0
	while turns < max_turns:
		#visual(bd)
		turns += 1
		mv = bd.get_moves()
		if mv == []:
			if a1 == bd.movpl:
				return 0
			return 1
		if a1 == bd.movpl:
			mov = agent1(bd,mv)
		else:
			mov = agent_ran(bd,mv)
		res = bd.apply_move(mov[0],mov[1],mov[2])
		if res[0] == True:
			if res[1] == a1:
				return 1
			return 0

for i in range(10):
	print(sim_game(0))
print()
for i in range(10):
	print(sim_game(1))


