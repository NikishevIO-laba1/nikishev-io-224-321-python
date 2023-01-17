#hw
#w=int(input('ширина'))
#h=int(input('высота'))
#f=input('Закрасить? y/n: ')
w=20
h=10
f='n'
is_fill=f.lower()=='y'
char_fill='█' if is_fill else ' '
char_frame=' ' if is_fill else '█'
print('змея')
for i in range(h):
    if i%2==0: print(char_frame*w)
    elif i%4==1 :print(char_fill*(w-1)+char_frame)
    else:print(char_frame+char_fill*(w-1))