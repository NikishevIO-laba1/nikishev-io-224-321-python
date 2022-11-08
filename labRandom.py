import random
#Вернуть псевдостлучайное дробной число в интервале [0.0, 1.0)
print(random.random())

#ВЕрнуть целое число в диапазонее от <начало> дл <конец>
#t
#ПЕремешать список 
print(random.randint(100,999))

print(random.randrange(100,999,100))
numbers=list(range(10))
print(numbers)
random.shuffle(numbers)
print(numbers)
#перемешать вернуть случайный элемент с последовательности(строка, список, ...)
print(random.choices("ПРИВЕТ"))
print(random.choices("ПРИВЕТ",k=20))
print(random.choices(list(range(10)),k=20))

# дрмшаняя работа оаставшиеся методы в рандоме

print(random.randbytes(4)) #байты 
print(random.sample("ПРИВЕТ", 4)) #неповторяющиеся элементы списк а
print(random.uniform(1, 4)) #случайное float в диапазоне
random.seed(100)#задание зерна
print(random.triangular(1, 10, 4)) #треугольное распределение, вершина в 4