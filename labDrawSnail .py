import numpy
def DrawSnail(size: int, orientation:str='l'):
    """улитка 

    size - размер, 

    orientation - 'l' или 'r' закручивается  влево или вправо соответственно"""
    snail=numpy.zeros((size,size), dtype=object)
    a,b=0,0
    a1,b1,start=size-1,size-1,True
    for i in range(int(size/2)):
        while a<a1:
            snail [a,b]=1
            a+=1
        a1-=2
        while b<b1:
            snail[a,b]=1
            b+=1
        b1-=2
        while snail[a-2,b]!=1:
            snail[a,b]=1
            a-=1
        if start is True:
            snail[a,b]=1
            a-=1
            start=False
        while snail[a,b-2]!=1:
            snail[a,b]=1
            b-=1
    if size%2==1: snail[a, b]=1
    if orientation=='l': snail=numpy.fliplr(numpy.rot90(snail, k=3  ))
    #if orientation=='r': snail=numpy.rot90(snail, k=2)
    snail[snail==0]='  '
    snail[snail==1]='██'
    for i in snail: print(''.join(i))

DrawSnail(11, 'l')