# дз вывести в консоль все доступные цвета и фоны
print('\x1b[6;30;42mПривет!\x1b[0m')
print('\x1b[6;30;40mПривет!\x1b[0m')
for a in range(30,38):
    for b in range(40,48):
        c=str(a)+';'+str(b)
        print('\x1b['+c+'m'+c+'\x1b[0m', end="")
    print()

print('#2')
for a in range (0,64): print("\x1b[", 30+a//8, ';', 40+a%8,'m', 30+a//8 , ';', 40+a%8,"\x1b[0m" ,'\n'*((a%8)-7==0) ,sep='', end='')