x=int(input('w '))
y=int(input('h '))
import random
matrix= []
for i in range(y): matrix.append( random.sample(range(10,100), x))
print (matrix)
what=int(input('1 влево2 вправо 3 отразить 4 отразить горизонатльно'))
if what ==1: print(*zip(*matrix))
if what ==2: print(list(zip(*matrix))[::-1])
if what ==3: print(*reversed(matrix))
if what ==4: print(*(list(reversed(i)) for i in matrix))

print('способ 2')
matrix= []
for i in range(y): matrix=matrix+ [random.sample(range(10,100), x)]
print (matrix)
if what ==1: matrix=list(map(list, zip(*matrix)))
if what ==2: matrix=list(map(list, zip(*matrix)))[::-1]
if what ==3: matrix=matrix[::-1]
if what ==4: matrix=list(i[::-1] for i in matrix)

print("вариант 3 с numpy")

