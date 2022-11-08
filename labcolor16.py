# дз вывести в консоль все доступные цвета и фоны
print('\x1b[6;30;42mПривет!\x1b[0m')
print('\x1b[6;30;40mПривет!\x1b[0m')
for a in range(30,38):
    for b in range(40,48):
        c=str(a)+';'+str(b)
        print('\x1b['+
        #str(b-40)+
        '0;'+c+'m'+c+'\x1b[0m', end="")
    print()