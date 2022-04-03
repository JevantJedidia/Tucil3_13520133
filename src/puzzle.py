from pohon import TreeNode

def readFile(fileName): #Membaca file dan mengubahnya menjadi matrix 15-puzzle
    puzzle = []
    with open(fileName, 'r') as f:
        puzzle = [[int(angka) for angka in line.split(' ')] for line in f]
    return puzzle

def printPuzzle(puzzle): #Mencetak 15-puzzle
    for i in range (4):
        for j in range (4):
            if (puzzle[i][j] == 16):
                if j < 3:
                    print(' -', end = " ")
                else:
                    print(' -', end = "\n")
            else:
                if j < 3:
                    if puzzle[i][j] < 10:
                        print(" " + str(puzzle[i][j]), end = " ")
                    else:
                        print(str(puzzle[i][j]), end = " ")
                else:
                    if puzzle[i][j] < 10:
                        print(" " + str(puzzle[i][j]), end = "\n")
                    else:
                        print(str(puzzle[i][j]), end = "\n")

def convertToMatIndex(index): #Mengubah angka menjadi indeks pada matriks
    row = index // 4
    col = index % 4
    return row, col

def getKurang(puzzle): #Mendapatkan nilai kurang(i) dan index dari bagian yang kosong
    kurang = []
    for i in range (16):
        row, col = convertToMatIndex(i)
        ubin = puzzle[row][col]
        counter = 0
        if ubin == 16:
            indexKosong = i
        for j in range (i+1,16):
            row1, col1 = convertToMatIndex(j)
            temp = puzzle[row1][col1]
            if temp != 16:
                if ubin > temp:
                    counter += 1
        kurang.append([ubin,counter])
    return kurang, indexKosong

def getXKosong(index): # Mendapatkan nilai X yang didapat dari bagian yang kosong
    arsir = [1,3,4,6,9,11,12,14]
    if index in arsir:
        return 1
    else:
        return 0

def countSolvable(kurang, indexKosong): #Menghitung total dari kurang(i) ditambah dengan nilai X
    X = getXKosong(indexKosong)
    for i in range (16):
        X += kurang[i][1]
    return X

def sortKurang(kurang): # Sort tabel kurang(i) sehingga i terurut menaik
    for i in range(16):
        if kurang[i][0] != i+1:
            for j in range (i,16):
                if kurang[j][0] == i+1:
                    temp = kurang[i]
                    kurang[i] = kurang[j]
                    kurang[j] = temp
                    break
        
def printKurang(kurang): #Mencetak kurang(i) dalam bentuk tabel
    print ("Ubin | Kurang(i)")
    print ("----------------")
    for i in range (16):
        if kurang[i][0] < 10:
            print (" " + str(kurang[i][0]) + "   |  " + str(kurang[i][1]))
        else:
            print (str(kurang[i][0]) + "   |  " + str(kurang[i][1]))

def indexKosong(puzzle): #Mencari indeks dari ubin yang kosong
    for i in range(16):
        row, col = convertToMatIndex(i)
        if puzzle[row][col] == 16:
            return row, col

def checkMoveValid(puzzle, direction): #Memeriksa apakah gerakan ubin kosong pada puzzle valid
    row, col = indexKosong(puzzle)
    if direction == "up":
        if row == 0:
            return False
        else:
            return True
    elif direction == "right":
        if col == 3:
            return False
        else:
            return True
    elif direction == "down":
        if row == 3:
            return False
        else:
            return True
    elif direction == "left":
        if col == 0:
            return False
        else:
            return True

def getCost(puzzle): #Mendapatkan cost dari anak 15-puzzle
    counter = 0
    for i in range (16):
        row, col = convertToMatIndex(i)
        if puzzle[row][col] != 16:
            if puzzle[row][col] != i+1:
                counter += 1
    return counter

def movePuzzle(puzzleOG, direction): #Menggerakan ubin kosong pada puzzle sesuai dengan arahnya
    puzzle = [row[:] for row in puzzleOG]
    row, col = indexKosong(puzzle)
    if direction == "up":
        temp = puzzle[row-1][col]
        puzzle[row-1][col] = puzzle[row][col]
        puzzle[row][col] = temp
    elif direction == "right":
        temp = puzzle[row][col+1]
        puzzle[row][col+1] = puzzle[row][col]
        puzzle[row][col] = temp
    elif direction == "down":
        temp = puzzle[row+1][col]
        puzzle[row+1][col] = puzzle[row][col]
        puzzle[row][col] = temp
    elif direction == "left":
        temp = puzzle[row][col-1]
        puzzle[row][col-1] = puzzle[row][col]
        puzzle[row][col] = temp
    return puzzle

def checkGoal(node): #Memeriksa apakah puzzle sudah sesuai dengan goal
    if node.cost - node.distance == 0:
        return True
    else:
        return False

def addSimpul(simpulHidup, node): #Menambahkan simpul hidup dengan basis prioQueue
    if len(simpulHidup) != 0:
        index = len(simpulHidup)
        for i in range(len(simpulHidup)):
            if simpulHidup[i].cost > node.cost:
                index = i
                break
        simpulHidup.insert(index,node)
    else:
        simpulHidup.append(node)

def printSolution(root, goal): #mencetak path dari solusi 15-puzzle
    print("Initial:")
    printPuzzle(root.puzzle)
    print("\n")
    currentNode = root
    for route in goal.path:
        for child in currentNode.children:
            if child.name == route:
                print(child.name)
                printPuzzle(child.puzzle)
                print("\n")
                currentNode = child
                break

def checkAccessed(accessed, puzzle): #Periksa apakah suatu state dari puzzle sudah pernah dibuat
    if puzzle in accessed:
        return True
    return False

def findSolution(puzzle): #mencari solusi dari 15-puzzle
    simpulHidup = []
    accessed = []
    found = False
    gerakan = ["up", "right", "down", "left"]
    root = TreeNode("root", puzzle, 0, 0, [])
    simpulHidup.append(root)
    accessed.append(root.puzzle)
    if checkGoal(root):
        found = True
        solution = root

    while (len(simpulHidup) != 0 and not found):
        currentNode = simpulHidup.pop(0)
        newDis = currentNode.distance+1
        for item in gerakan:
            newPath = currentNode.path.copy()
            if checkMoveValid(currentNode.puzzle, item):
                newPuzzle = movePuzzle(currentNode.puzzle,item)
                if not checkAccessed(accessed, newPuzzle):
                    newPath.append(item)
                    accessed.append(newPuzzle)
                    child = TreeNode(item, newPuzzle, newDis, getCost(newPuzzle), newPath)
                    currentNode.addChild(child)
                    addSimpul(simpulHidup,child)
                    
                    if checkGoal(child):
                        found = True
                        solution = child
                        break

    printSolution(root, solution)