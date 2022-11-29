w=30
h=6
fill=0.5%1
#w=input()*2
#h=input()*2
#fill=input()%1
import numpy
a=numpy.zeros([h,w], dtype=object)
n=0
for i in a: 
    n+=1
    i[::2]=abs(1-(n%2==0))
a=numpy.pad(a, (1,0), constant_values=0)
a=numpy.pad(a, 1, constant_values=1)
zeroes= a ==0
s=[0,0]
import random
for i in range(int(numpy.count_nonzero(zeroes)*fill)):
    s=[random.randint(1,h+1), random.randint(1,w+1)]
    while a[s[0],s[1]]==2 or a[s[0],s[1]]==1: 
        s=[random.randint(1,h+1), random.randint(1,w+1)]
    a[s[0],s[1]]=2

a[a==0]='  '
a[a==1]='██'
a[a==2]='▒▒'
for i in a: print(''.join(i))