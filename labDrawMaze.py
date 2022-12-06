
import numpy
def cls():
    """функция чтобы очистить терминал"""
    import os
    os.system('cls' if os.name=='nt' else 'clear')
import time
def show(a, s, speed):
    """вывод лабиринта, 
    
    a - массив, s - текущая позиция, speed - скорость"""
    n=numpy.copy(a)
    cls()
    n[s[0],s[1]]='$$'
    n[n==0]='  '
    n[n==1]='██'
    n[n==3]='██'
    n[n==2]='  '
    for i in n: print(''.join(i))
    print(a[s[0], s[1]], a[s[0]+1,s[1]], a[s[0]-1,s[1]], a[s[0],s[1]+1], a[s[0],s[1]-1])
    #time.sleep(speed)
def maze(h: int, w: int, visualize: bool=False):
    '''создаёт лабиринт и выводит на экран, 
    
    w - высота, 
    
    h -ширина, 
    
    visualize - True/False - визуализировать создание лабиринта (гораздо медленнее и очищает терминал)'''
    a=numpy.zeros([h-2,w-2], dtype=object)
    n=0
    for i in a: 
        n+=1
        i[::2]=abs(1-(n%2==0))
    a=numpy.pad(a, (1,0), constant_values=0)
    a=numpy.pad(a, 1, constant_values=3)
    import random
    start=random.randint(2,h-3)
    end=random.randint(2,h-3)
    start=start-((start+1)%2==1)
    end=end-((end+1)%2==1)
    s=[start,1]
    import time
    prev=None
    while True:
        n=0
        while a[s[0],s[1]]!=2:
            a[s[0],s[1]]=2
            walls=[]
            if a[s[0]+1,s[1]]==0: walls.append('u')
            if a[s[0]-1,s[1]]==0: walls.append('d')
            if a[s[0],s[1]+1]==0: walls.append('r')
            if a[s[0],s[1]-1]==0: walls.append('l')
            if prev=='u': 
                try:walls.remove('d')
                except ValueError:pass
            if prev=='d': 
                try:walls.remove('u')
                except ValueError:pass    
            if prev=='l': 
                try:walls.remove('r')
                except ValueError:pass
            if prev=='r': 
                try:walls.remove('l')
                except ValueError:pass            
            if walls==[]:break
            d=random.choice(walls) #u d r
            #print(d, walls, prev, n)
            if d=='u':
                if prev!='u': a[s[0]-1,s[1]]=1
                if prev!='r':a[s[0],s[1]-1]=1
                if prev!='l':a[s[0],s[1]+1]=1
                s[0]+=2
            if d=='d':
                if prev!='d': a[s[0]+1,s[1]]=1
                if prev!='r': a[s[0],s[1]-1]=1
                if prev!='l': a[s[0],s[1]+1]=1
                s[0]-=2
            if d=='r':
                if prev!='d':  a[s[0]+1,s[1]]=1
                if prev!='u': a[s[0]-1,s[1]]=1
                if prev!='r': a[s[0],s[1]-1]=1
                s[1]+=2
            if d=='l':
                if prev!='d': a[s[0]+1,s[1]]=1
                if prev!='u': a[s[0]-1,s[1]]=1
                if prev!='l': a[s[0],s[1]+1]=1
                s[1]-=2
            if visualize is True: show(a, s, 0.01)

            prev=d
        s=[random.randint(2,h-2),random.randint(2,w-2)]
        s[0]+=(s[0]%2==0)
        s[1]+=(s[1]%2==0)
        if visualize is True: show(a, s, 0.01)
        stop=False
        while a[s[0], s[1]]==2 or (a[s[0]+1,s[1]]!=1 and a[s[0]-1,s[1]]!=1 and a[s[0],s[1]+1]!=1 and a[s[0],s[1]-1]!=1):
            s=[random.randint(2,h-2),random.randint(2,w-2)]
            s[0]+=(s[0]%2==0)
            s[1]+=(s[1]%2==0)
            n+=1
            if n==w*h:
                stop=True
                break
        if stop is True: break
        walls=[]
        if a[s[0]+1,s[1]]==1: walls.append('u')
        if a[s[0]-1,s[1]]==1: walls.append('d')
        if a[s[0],s[1]+1]==1: walls.append('r')
        if a[s[0],s[1]-1]==1: walls.append('l')
        if walls==[]:continue
        d=random.choice(walls)
        if d=='u':
            a[s[0]+1,s[1]]=0
            prev='d'
        if d=='d':
            a[s[0]-1,s[1]]=0
            prev='u'
        if d=='r':
            a[s[0],s[1]+1]=0
            prev='l'
        if d=='l':
            a[s[0],s[1]-1]=0
            prev='r'

    a[start,0]=0
    a[end,w]=0
    a[a==0]='  '
    a[a==1]='██'
    a[a==3]='██'
    a[a==2]='  '
    cls()
    for i in a: print(''.join(i))


#h=input()*2
#w=input()*2
maze (h=20, w=50, visualize=False)
#maze(h=20, w=50, visualize=True)