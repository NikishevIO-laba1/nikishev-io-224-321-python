x=int(input('w '))
y=int(input('h '))
for i in range(y):
    for j in range(x):
        if (i+j)%2==0:print('██', end='')
        else: print('  ', end='')
    print()