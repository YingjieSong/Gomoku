grid_size = 40
 
w = 14
flag = True
black_win = False
white_win = False
game_over = False
Matrix = [[0 for x in range(-5,w+5)] for x in range(-5,w+5)]
L = []

import pygame

def new_game(w):
	global flag
	global black_win
	global white_win
	global game_over
	global Matrix
	global L
	global window

	flag = True
	black_win = False
	white_win = False
	game_over = False

	Matrix = [[0 for x in range(-5,w+5)] for x in range(-5,w+5)]
	while len(L) != 0:
		L.pop()

	pygame.init()
	window = pygame.display.set_mode((grid_size * (w+2),grid_size * (w+2)))
	window.fill((127,127,127))
	pygame.draw.rect(window,(0,0,0),(grid_size-5,grid_size-5,grid_size * w+10,grid_size * w+10),2)

	for i in range(w):
		for j in range(w):
			pygame.draw.rect(window,(0,0,0),(grid_size * (j+1),grid_size * (i+1),grid_size+1,grid_size+1),1)
			if i == 3 and (j == 3 or j == w-3) or i == w-3 and (j == 3 or j == w-3) or i == w/2 and j == w/2:
				pygame.draw.circle(window,(0,0,0),(grid_size * (j+1),grid_size * (i+1)),5)

	font = pygame.font.SysFont("Times New Roman", 20)
	string = "NEW GAME 15x15"
	text = font.render(string, 1, (255, 255, 255),(0, 0, 0))
	window.blit(text, (0, 0))

	font = pygame.font.SysFont("Times New Roman", 20)
	string = "19x19 NEW GAME"
	text = font.render(string, 1, (255, 255, 255),(0, 0, 0))
	window.blit(text, (grid_size * (w-2), 0))

	font = pygame.font.SysFont("Times New Roman", 20)
	string = "RETRACT"
	text = font.render(string, 1, (255, 255, 255),(0, 0, 0))
	window.blit(text, (grid_size * (w+0.1)//2, grid_size * (w+1.45)))

	pygame.display.update()
	game_over = draw_win(black_win,white_win)

def draw_black(mx_w, my_w):
	if mx_w in range(1,w+2) and my_w in range(1,w+2):
		mx=mx_w*grid_size
		my=my_w*grid_size
		pygame.draw.circle(window,(0,0,0),(mx,my),18)
		pygame.display.update()

		Matrix[my_w-1][mx_w-1] = 1

		L.append([my_w-1,mx_w-1])
		
		return False
	else:
		return True

def draw_white(mx_w,my_w):
	if mx_w in range(1,w+2) and my_w in range(1,w+2):
		mx=mx_w*grid_size
		my=my_w*grid_size
		pygame.draw.circle(window,(255,255,255),(mx,my),18)
		pygame.display.update()

		Matrix[my_w-1][mx_w-1] = 2

		L.append([my_w-1,mx_w-1])
		
		return True
	else:
		return False

def retract():
	global black_win
	global white_win
	global game_over

	if len(L) != 0:
		retract = L.pop()
		
		Matrix[retract[0]][retract[1]] = 0
		
		black_win = False
		white_win = False
		game_over = False

		window.fill((127,127,127))
		pygame.draw.rect(window,(0,0,0),(grid_size-5,grid_size-5,grid_size * w+10,grid_size * w+10),2)

		for i in range(w):
			for j in range(w):
				pygame.draw.rect(window,(0,0,0),(grid_size * (j+1),grid_size * (i+1),grid_size+1,grid_size+1),1)
				if i == 3 and (j == 3 or j == w-3) or i == w-3 and (j == 3 or j == w-3) or i == w/2 and j == w/2:
					pygame.draw.circle(window,(0,0,0),(grid_size * (j+1),grid_size * (i+1)),5)

		for i in range(-5,w+5):
			for j in range(-5,w+5):
				if Matrix[i][j] == 1:
					pygame.draw.circle(window,(0,0,0),((j+1)*grid_size,(i+1)*grid_size),18)
				elif Matrix[i][j] == 2:
					pygame.draw.circle(window,(255,255,255),((j+1)*grid_size,(i+1)*grid_size),18)

		font = pygame.font.SysFont("Times New Roman", 20)
		string = "NEW GAME 15x15"
		text = font.render(string, 1, (255, 255, 255),(0, 0, 0))
		window.blit(text, (0, 0))

		font = pygame.font.SysFont("Times New Roman", 20)
		string = "19x19 NEW GAME"
		text = font.render(string, 1, (255, 255, 255),(0, 0, 0))
		window.blit(text, (grid_size * (w-2), 0))

		font = pygame.font.SysFont("Times New Roman", 20)
		string = "RETRACT"
		text = font.render(string, 1, (255, 255, 255),(0, 0, 0))
		window.blit(text, (grid_size * (w+0.1)//2, grid_size * (w+1.45)))

		pygame.display.update()

		return not flag

	else:
		return flag

def check_black(mx_w, my_w):
	#check row
	if Matrix[my_w-1][mx_w] == 1 and Matrix[my_w-1][mx_w+1] == 1 and Matrix[my_w-1][mx_w+2] == 1 and Matrix[my_w-1][mx_w+3] == 1:
		return True
	elif Matrix[my_w-1][mx_w] == 1 and Matrix[my_w-1][mx_w+1] == 1 and Matrix[my_w-1][mx_w+2] == 1 and Matrix[my_w-1][mx_w-2] == 1:
		return True
	elif Matrix[my_w-1][mx_w] == 1 and Matrix[my_w-1][mx_w+1] == 1 and Matrix[my_w-1][mx_w-2] == 1 and Matrix[my_w-1][mx_w-3] == 1:
		return True
	elif Matrix[my_w-1][mx_w] == 1 and Matrix[my_w-1][mx_w-2] == 1 and Matrix[my_w-1][mx_w-3] == 1 and Matrix[my_w-1][mx_w-4] == 1:
		return True
	elif Matrix[my_w-1][mx_w-2] == 1 and Matrix[my_w-1][mx_w-3] == 1 and Matrix[my_w-1][mx_w-4] == 1 and Matrix[my_w-1][mx_w-5] == 1:
		return True

	#check column
	if Matrix[my_w][mx_w-1] == 1 and Matrix[my_w+1][mx_w-1] == 1 and Matrix[my_w+2][mx_w-1] == 1 and Matrix[my_w+3][mx_w-1] == 1:
		return True
	elif Matrix[my_w][mx_w-1] == 1 and Matrix[my_w+1][mx_w-1] == 1 and Matrix[my_w+2][mx_w-1] == 1 and Matrix[my_w-2][mx_w-1] == 1:
		return True
	elif Matrix[my_w][mx_w-1] == 1 and Matrix[my_w+1][mx_w-1] == 1 and Matrix[my_w-2][mx_w-1] == 1 and Matrix[my_w-3][mx_w-1] == 1:
		return True
	elif Matrix[my_w][mx_w-1] == 1 and Matrix[my_w-2][mx_w-1] == 1 and Matrix[my_w-3][mx_w-1] == 1 and Matrix[my_w-4][mx_w-1] == 1:
		return True
	elif Matrix[my_w-2][mx_w-1] == 1 and Matrix[my_w-3][mx_w-1] == 1 and Matrix[my_w-4][mx_w-1] == 1 and Matrix[my_w-5][mx_w-1] == 1:
		return True

	#check top-left to bottom-right
	if Matrix[my_w][mx_w] == 1 and Matrix[my_w+1][mx_w+1] == 1 and Matrix[my_w+2][mx_w+2] == 1 and Matrix[my_w+3][mx_w+3] == 1:
		return True
	elif Matrix[my_w][mx_w] == 1 and Matrix[my_w+1][mx_w+1] == 1 and Matrix[my_w+2][mx_w+2] == 1 and Matrix[my_w-2][mx_w-2] == 1:
		return True		
	elif Matrix[my_w][mx_w] == 1 and Matrix[my_w+1][mx_w+1] == 1 and Matrix[my_w-2][mx_w-2] == 1 and Matrix[my_w-3][mx_w-3] == 1:
		return True
	elif Matrix[my_w][mx_w] == 1 and Matrix[my_w-2][mx_w-2] == 1 and Matrix[my_w-3][mx_w-3] == 1 and Matrix[my_w-4][mx_w-4] == 1:
		return True
	elif Matrix[my_w-2][mx_w-2] == 1 and Matrix[my_w-3][mx_w-3] == 1 and Matrix[my_w-4][mx_w-4] == 1 and Matrix[my_w-5][mx_w-5] == 1:
		return True

	#check top-right to bottom-left
	if Matrix[my_w-2][mx_w] == 1 and Matrix[my_w-3][mx_w+1] == 1 and Matrix[my_w-4][mx_w+2] == 1 and Matrix[my_w-5][mx_w+3] == 1:
		return True
	elif Matrix[my_w-2][mx_w] == 1 and Matrix[my_w-3][mx_w+1] == 1 and Matrix[my_w-4][mx_w+2] == 1 and Matrix[my_w][mx_w-2] == 1:
		return True
	elif Matrix[my_w-2][mx_w] == 1 and Matrix[my_w-3][mx_w+1] == 1 and Matrix[my_w][mx_w-2] == 1 and Matrix[my_w+1][mx_w-3] == 1:
		return True
	elif Matrix[my_w-2][mx_w] == 1 and Matrix[my_w][mx_w-2] == 1 and Matrix[my_w+1][mx_w-3] == 1 and Matrix[my_w+2][mx_w-4] == 1:
		return True
	elif Matrix[my_w][mx_w-2] == 1 and Matrix[my_w+1][mx_w-3] == 1 and Matrix[my_w+2][mx_w-4] == 1 and Matrix[my_w+3][mx_w-5] == 1:
		return True

def check_white(mx_w, my_w):
	#check row
	if Matrix[my_w-1][mx_w] == 2 and Matrix[my_w-1][mx_w+1] == 2 and Matrix[my_w-1][mx_w+2] == 2 and Matrix[my_w-1][mx_w+3] == 2:
		return True
	elif Matrix[my_w-1][mx_w] == 2 and Matrix[my_w-1][mx_w+1] == 2 and Matrix[my_w-1][mx_w+2] == 2 and Matrix[my_w-1][mx_w-2] == 2:
		return True
	elif Matrix[my_w-1][mx_w] == 2 and Matrix[my_w-1][mx_w+1] == 2 and Matrix[my_w-1][mx_w-2] == 2 and Matrix[my_w-1][mx_w-3] == 2:
		return True
	elif Matrix[my_w-1][mx_w] == 2 and Matrix[my_w-1][mx_w-2] == 2 and Matrix[my_w-1][mx_w-3] == 2 and Matrix[my_w-1][mx_w-4] == 2:
		return True
	elif Matrix[my_w-1][mx_w-2] == 2 and Matrix[my_w-1][mx_w-3] == 2 and Matrix[my_w-1][mx_w-4] == 2 and Matrix[my_w-1][mx_w-5] == 2:
		return True

	#check column
	if Matrix[my_w][mx_w-1] == 2 and Matrix[my_w+1][mx_w-1] == 2 and Matrix[my_w+2][mx_w-1] == 2 and Matrix[my_w+3][mx_w-1] == 2:
		return True
	elif Matrix[my_w][mx_w-1] == 2 and Matrix[my_w+1][mx_w-1] == 2 and Matrix[my_w+2][mx_w-1] == 2 and Matrix[my_w-2][mx_w-1] == 2:
		return True
	elif Matrix[my_w][mx_w-1] == 2 and Matrix[my_w+1][mx_w-1] == 2 and Matrix[my_w-2][mx_w-1] == 2 and Matrix[my_w-3][mx_w-1] == 2:
		return True
	elif Matrix[my_w][mx_w-1] == 2 and Matrix[my_w-2][mx_w-1] == 2 and Matrix[my_w-3][mx_w-1] == 2 and Matrix[my_w-4][mx_w-1] == 2:
		return True
	elif Matrix[my_w-2][mx_w-1] == 2 and Matrix[my_w-3][mx_w-1] == 2 and Matrix[my_w-4][mx_w-1] == 2 and Matrix[my_w-5][mx_w-1] == 2:
		return True

	#check top-left to bottom-right
	if Matrix[my_w][mx_w] == 2 and Matrix[my_w+1][mx_w+1] == 2 and Matrix[my_w+2][mx_w+2] == 2 and Matrix[my_w+3][mx_w+3] == 2:
		return True
	elif Matrix[my_w][mx_w] == 2 and Matrix[my_w+1][mx_w+1] == 2 and Matrix[my_w+2][mx_w+2] == 2 and Matrix[my_w-2][mx_w-2] == 2:
		return True		
	elif Matrix[my_w][mx_w] == 2 and Matrix[my_w+1][mx_w+1] == 2 and Matrix[my_w-2][mx_w-2] == 2 and Matrix[my_w-3][mx_w-3] == 2:
		return True
	elif Matrix[my_w][mx_w] == 2 and Matrix[my_w-2][mx_w-2] == 2 and Matrix[my_w-3][mx_w-3] == 2 and Matrix[my_w-4][mx_w-4] == 2:
		return True
	elif Matrix[my_w-2][mx_w-2] == 2 and Matrix[my_w-3][mx_w-3] == 2 and Matrix[my_w-4][mx_w-4] == 2 and Matrix[my_w-5][mx_w-5] == 2:
		return True

	#check top-right to bottom-left
	if Matrix[my_w-2][mx_w] == 2 and Matrix[my_w-3][mx_w+1] == 2 and Matrix[my_w-4][mx_w+2] == 2 and Matrix[my_w-5][mx_w+3] == 2:
		return True
	elif Matrix[my_w-2][mx_w] == 2 and Matrix[my_w-3][mx_w+1] == 2 and Matrix[my_w-4][mx_w+2] == 2 and Matrix[my_w][mx_w-2] == 2:
		return True
	elif Matrix[my_w-2][mx_w] == 2 and Matrix[my_w-3][mx_w+1] == 2 and Matrix[my_w][mx_w-2] == 2 and Matrix[my_w+1][mx_w-3] == 2:
		return True
	elif Matrix[my_w-2][mx_w] == 2 and Matrix[my_w][mx_w-2] == 2 and Matrix[my_w+1][mx_w-3] == 2 and Matrix[my_w+2][mx_w-4] == 2:
		return True
	elif Matrix[my_w][mx_w-2] == 2 and Matrix[my_w+1][mx_w-3] == 2 and Matrix[my_w+2][mx_w-4] == 2 and Matrix[my_w+3][mx_w-5] == 2:
		return True

def draw_win(black_win,white_win):
	font = pygame.font.SysFont("Times New Roman", 20)
	if black_win:
		string = "BLACK WIN!"
		text = font.render(string, 1, (255,0,0),(127,127,127))
	elif white_win:
		string = "WHITE WIN!"
		text = font.render(string, 1, (255,0,0),(127,127,127))
	elif flag:
		string = "     BLACK     "
		text = font.render(string, 1, (0,0,0),(127,127,127))
	elif not flag:
		string = "     WHITE     "
		text = font.render(string, 1, (255,255,255),(127,127,127))
	window.blit(text, (grid_size * (w/2)-15,0))
	pygame.display.update()

	if black_win or white_win:
		return True

new_game(w)
game_over = draw_win(black_win,white_win)
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				(x, y) = event.pos
				mx_w=(x+grid_size//2)//grid_size
				my_w=(y+grid_size//2)//grid_size
				if x<160 and y<25:
					pygame.quit()
					w=14
					new_game(w)	#15x15
				elif x in range(grid_size * (w-2),grid_size * (w+2)) and y<25:
					pygame.quit()
					w=18
					new_game(w)	#19x19
				elif x in range(grid_size * (w)//2+grid_size//20,grid_size * (w+4)//2-grid_size//20) and y>grid_size * (w+1.45):
					flag = retract()
					game_over = draw_win(black_win,white_win)
				elif not game_over:
					if Matrix[my_w-1][mx_w-1] != 0:
						continue
					if flag:
						flag = draw_black(mx_w, my_w)
						black_win = check_black(mx_w, my_w)
					else:
						flag = draw_white(mx_w, my_w)
						white_win = check_white(mx_w, my_w)
					game_over = draw_win(black_win,white_win)