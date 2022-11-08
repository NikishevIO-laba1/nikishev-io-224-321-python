#ДОМАШНЕЕ ЗАДАНИЕ ВЫВСЕТИ В КОНСОЛЬ ВСЕ ДОСТУПНЫЕ ЦВЕТА И ФОНЫ
print('\x1b[6;30;42mПривет!\x1b[0m')
print('\x1b[6;30;40mПривет!\x1b[0m')
for a in range(30,38):
    for b in range(40,48):
        c=str(a)+';'+str(b)
        print('\x1b[6;'+c+'m'+c+'\x1b[0m', end="")
    print()