#abDrawTableANSII - вывести в консоль таблицу из ansii-символов с параметрами: колонок, строк
def ansii (columns, lines):
    for i in range(lines*columns):
        print(chr(i), end=' ')
        if i%columns==columns-1: print()
ansii(50,100)