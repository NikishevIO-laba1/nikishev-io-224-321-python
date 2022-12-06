while True:
    t,f,mode, difficulty=0,0,0,0
    while mode!=10 and mode!=16: mode=int(input('Выберите режим игры: "10" - ответ десятичным числом; "16" - ответ шестнадцатеричным числом. '))
    while difficulty<1 or difficulty>4: difficulty=int(input('выбрать: уровень сложности: "1", "2", "3", или "4". 1, детский: числа от 0000 0000 до 0000 0111; 2, легкий: числа от 0000 0000 до 0000 1111; 3, средний: числа от 0000 0000 до 0011 1111; 4, сложный: числа от 0000 0000 до 1111 1111. '))
    amount=int(input('введите количество вопросов: '))
    if difficulty==1: difficulty =  0b111
    elif difficulty==2: difficulty =  0b1111
    elif difficulty==3: difficulty =  0b111111
    else:difficulty =  0b11111111
    import random,time
    start=time.time()
    for i in range(amount):
        n=random.randint(0,difficulty)
        if mode==16: n= hex(n)
        a=int(input(f'Введите: {bin(n)[2:]} в {mode}-ричной системе счисления = '))
        if a==n:
            print('верно')
            t+=1
        else: 
            print('неверно. Правильный ответ:', n)
            f+=1
    t=input (f'{t} верных ответов, {f} неверных ответов, общее время: {time.time()-start} секунд. Сыграть снова? (y/n): ')
    if t.lower()=='n' or t.lower()=='no' or t.lower()=='н' or t.lower()=='нет': break