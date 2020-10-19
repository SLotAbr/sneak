from tkinter import *
import random
import time


tk = Tk()
tk.title("Sneak")
tk.resizable(0, 0)  # The window size becomes fixed
tk.wm_attributes("-topmost", 1)  # The canvas window is placed on top of all other windows ("–topmost")
canvas = Canvas(tk, width=500, height=500, bd=0,highlightthickness=0)
canvas.pack()  # After this command, the canvas resizes according to the specified parameters


class Sneak():
	def __init__(self):
		self.canvas = canvas

		self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
		self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
		self.canvas.bind_all('<KeyPress-Up>', self.turn_up)
		self.canvas.bind_all('<KeyPress-Down>', self.turn_down)

	def turn_left(self,evt):
		global move_vector
		move_vector=-1

	def turn_right(self,evt):
		global move_vector
		move_vector=1

	def turn_up(self,evt):
		global move_vector
		move_vector=-SIZE

	def turn_down(self,evt):
		global move_vector
		move_vector=SIZE


def UpdateCoord():
	global NewCoord
	global PastCoord
	global move_vector

	NewCoord[0]+=move_vector

	for i in range(1,len(NewCoord)):
		NewCoord[i]=PastCoord[i-1]


def UpdatePastCoord():
	global NewCoord
	global PastCoord

	for i in range(0,len(NewCoord)):
		PastCoord[i]=NewCoord[i]


#Изменяет типы клеток в соответсвии с UpdateCoord
#И запускает их отрисовку
def Main():
	global BaseCells
	global TypeCells
	global NewCoord
	global spawn_food
	global SIZE
	global Game

	#Проверка столкновения с собой или блоком
	if (TypeCells[NewCoord[0]]==2) or (TypeCells[NewCoord[0]]==4):
		Game=0
	#Перед отрисовкой клеток на новом этапе происходит
	#очищение старых клеток со змейкой
	for i in range(0,len(PastCoord)):
		TypeCells[PastCoord[i]]=0
		BaseCells[PastCoord[i]].config(bg='gray')
	
	#Проверка наличия клетки пищи под головой змейки
	if TypeCells[NewCoord[0]]==3:
		NewCoord.append(PastCoord[len(PastCoord)-1])
		PastCoord.append(PastCoord[len(PastCoord)-1])

		#При спавне блока пищи возможен баг, связанный с
		#поеданием 2 подряд идущих блоков еды (В этом случае PastCoord
		#не успевает обновиться)
		while True:
			k=random.randint(0,SIZE**2)
			if TypeCells[k]==0:
				TypeCells[k]=3
				BaseCells[k].config(bg='green')
				break
				
	TypeCells[NewCoord[0]]=1
	BaseCells[NewCoord[0]].config(bg='red')

	for i in range(1,len(NewCoord)):
		TypeCells[NewCoord[i]]=2
		BaseCells[NewCoord[i]].config(bg='orange')
		

SIZE=25
SIZE_CELL=20
BaseCells=[x*0 for x in range(SIZE**2)]  # Cell field formation
for i in range(SIZE):
	for j in range(SIZE):
		BaseCells[i*SIZE + j]=Button(tk,bg='gray')
		BaseCells[i*SIZE + j].place(x=SIZE_CELL*j,
									y=SIZE_CELL*i, 
									width=SIZE_CELL, 
									height=SIZE_CELL)

TypeCells=[x*0 for x in range(SIZE**2)] 

Game=1
move_vector=0
Sn=Sneak()

NewCoord=[80,79,78]
PastCoord=[80,79,78]

TypeCells[120]=3
BaseCells[120].config(bg='green')

# Bounding field formation
for i in range(SIZE):
	TypeCells[i]=4
	TypeCells[i*SIZE]=4
	TypeCells[i*SIZE-1]=4
	TypeCells[SIZE*(SIZE-1)+i]=4
	BaseCells[i].config(bg='black')
	BaseCells[i*SIZE].config(bg='black')
	BaseCells[i*SIZE-1].config(bg='black')
	BaseCells[SIZE*(SIZE-1)+i].config(bg='black')

Main()
while 1:
	if (move_vector!=0) and (Game==1):
		UpdateCoord()
		Main()
		UpdatePastCoord()
	
	tk.update_idletasks()
	tk.update()
	time.sleep(0.1)