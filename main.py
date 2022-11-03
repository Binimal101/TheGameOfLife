from pprint import pprint
from time import sleep
import os

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

clearConsole()

def newSeries(generation, cells):
	with open(f"series/gospelGun/{generation}.jpg", "wb") as fp:
		print([y*11111111 for x in cells for y in x]) #fully white or black pixels
		bits = bytes([y for x in cells for y in x])
		fp.write(bits) #How does the file format work?

def htmlize(array):
	s = []
	for row in array:
		for cell in row:
			s.append('▓▓' if cell else '░░')
		s.append("\n")
	return ''.join(s)

def get_generation(cells, generations):
	cellsCopy = cells.copy()
	cellsCopy = grow(cellsCopy) if generations else cellsCopy
	nextCells = []
	nextCellRow = []
	# newSeries(0, cellsCopy)
	print(0, "\n" + htmlize(cellsCopy))
	for generation in range(1, generations+1):
		for cellRowNum, cellRow in enumerate(cellsCopy):
			for cellColNum, cell in enumerate(cellRow):
				
				alive, _ = getSurrounding(cellsCopy, cellRowNum, cellColNum)
				
				if cellsCopy[cellRowNum][cellColNum]: #Current Cell is alive
					if alive < 2 or alive > 3:
						nextCellRow.append(0) #Live cell death due to over/under pop
					
					else:
						nextCellRow.append(1) #current live cell lives on
				
				else: #Current Cell is dead
					if alive == 3: #Reproduction rules
						nextCellRow.append(1) #Cell is 'resurrected'
					else:
						nextCellRow.append(0) #Cell stays dead
                        
			nextCells.append(nextCellRow)
			nextCellRow = []
		cellsCopy = grow(crop(nextCells))
		nextCells = []
		
		# newSeries(generation, cellsCopy)
		print(generation, "\n" + htmlize(cellsCopy))
		sleep(0.4)
		if len(cellsCopy[0]) > 68: #so we don't get wrapping off of the sides of the console, but still maintain a big img
			return
	return crop(cellsCopy)

def getSurrounding(cells, row, col):
    surrounding = []    
    
    #Top right of target
    if row < len(cells)-1 and col < len(cells[row])-1:
        tr = (cells[row+1][col+1], {
            "row" : row+1,
            "col" : col+1,
        })
    else:
        tr = None
        
    #Top left of target
    if row < len(cells)-1 and col != 0:
        tl = (cells[row+1][col-1], {
            "row" : row+1,
            "col" : col-1,
        })
    else:
        tl = None
    
    #Above target
    if row < len(cells)-1:    
        above = (cells[row+1][col], {
            "row" : row+1,
            "col" : col,
        })
    else:
        above = None
        

    #To the right of target
    if col < len(cells[row])-1:
        right = (cells[row][col+1], {
            "row" : row,
            "col" : col+1,
        })
    else:
        right = None
    
    #To the left of target
    if col != 0:
        left = (cells[row][col-1], {
            "row" : row,
            "col" : col-1,
        })
    else:
        left = None
    
    #Below target
    if row != 0:
        below = (cells[row-1][col], {
            "row" : row-1,
            "col" : col,
        })
    else:
        below = None
        
    #Bottom left of target
    if row != 0 and col != 0:
        bl = (cells[row-1][col-1], {
            "row" : row-1,
            "col" : col-1,
        })
    else:
        bl = None
    
    #Bottom right of target
    if row != 0 and col < len(cells[row])-1:
        br = (cells[row-1][col+1], {
            "row" : row-1,
            "col" : col+1,
        })
    else:
        br = None
        
    
        
    surrounding = [x for x in [tl, tr, above, below, right, left, bl, br] if x is not None]
    surrounding = ([x[0] for x in surrounding].count(1), surrounding)

    return surrounding



def crop(cells): 
    
    while not 1 in cells[0]:
        del cells[0]
        
    while not 1 in cells[-1]:
        del cells[-1]
        
    columns = [list(x) for x in list(zip(*cells))]
    
    while not 1 in columns[0]:
        del columns[0]
    
    while not 1 in columns[-1]:
        del columns[-1]
            
    return [list(x) for x in list(zip(*columns))] #go back to rows

def grow(cells):
    
    if 1 in cells[0]:
        cells.insert(0, [int(x) for x in "0"*len(cells[0])])
        
    if 1 in cells[-1]:
        cells.append([int(x) for x in "0"*len(cells[0])])
        
    columns = [list(x) for x in list(zip(*cells))]

    if 1 in columns[0]:
        columns.insert(0, [int(x) for x in "0"*len(columns[0])])
    
    if 1 in columns[-1]:
        columns.append([int(x) for x in "0"*len(columns[-1])]) 

    return [list(x) for x in list(zip(*columns))]

def gospelGun():
	gospelGun = [
		[int(x) for x in "0000000000000000000000000001100000000000"],
						# ---------------------------XX-----------
		[int(x) for x in "0000000000000000000000000010001000000000"],
						# --------------------------X---X---------
		[int(x) for x in "0000000000110000000000000100000100011000"],
						# ----------XX-------------X-----X---XX---
		[int(x) for x in "0000000000110000000000000100010110011000"],
						# ----------XX-------------X---X-XX--XX---
		[int(x) for x in "0110001000000110000000000100000100000000"],
						# -XX---X------XX----------X-----X--------
		[int(x) for x in "0101000100000111000000000010001000000000"],
						# -X-X---X-----XXX----------X---X---------
		[int(x) for x in "0011111000000110000000000001100000000000"],
						# --XXXXX------XX------------XX-----------
		[int(x) for x in "0001110000110000000001010000000000000000"],
						# ---XXX----XX---------X-X----------------
		[int(x) for x in "0000000000110000000000110000000000000000"],
						# ----------XX----------XX----------------
		[int(x) for x in "0000000000000000000000100000000000000000"],
						# ----------------------X-----------------
	]
	get_generation(gospelGun, 200)

gospelGun()
