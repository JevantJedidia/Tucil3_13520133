from puzzle import *
from pohon import *
import time

fileName = input("Masukkan nama file: ")
puzzle = readFile("testcase/" + fileName)

# Nomor 1
print("Matrix awal: ")
printPuzzle(puzzle)
print("\n")

# Nomor 2
start = time.time()
kurang, indexKosong = getKurang(puzzle)
sortKurang(kurang)
end = time.time()
totalTime = end-start
printKurang(kurang)

# Nomor 3
print("Nilai dari KURANG(i) + X:", end = " ")
start = time.time()
X = countSolvable(kurang, indexKosong)
end = time.time()
totalTime += end-start
print(X)
print("\n")

if X % 2 == 0:
    # Nomor 5
    start = time.time()
    findSolution(puzzle)
    end = time.time()
    totalTime += end-start
else:
    # Nomor 4
    print("Tidak dapat diselesaikan")

# Nomor 6
print("Waktu eksekusi program: " + str(totalTime) + " s")

# Nomor 7
if X % 2 == 0:
    print("Jumlah simpul yang dibangkitkan: " + str(TreeNode.id-1))
    print("\n")
else:
    print("Jumlah simpul yang dibangkitkan: 0" )
    print("\n")
    