#hw
char = '█'
w=int(input('ширина'))
h=int(input('высота'))
f=input('Закрасить? y/n: ')
is_fill=f.lower()=='y'
char_fill=char if is_fill else ' '
for r in range(h):
    print(char*w)
    #hw сделать так чтобы была рамка