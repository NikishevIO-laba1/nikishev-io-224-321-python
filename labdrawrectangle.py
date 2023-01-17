#hw
#w=int(input('ширина'))
#h=int(input('высота'))
#f=input('Закрасить? y/n: ')
w=20
h=10
f='n'
is_fill=f.lower()=='y'
char_fill='█' if is_fill else ' '
#for r in range(h):
    #print(char_fill*w)
    #hw сделать так чтобы была рамка

print('#1')
char_frame=' ' if is_fill else '█'
for r in range(h):
    if r==0 or r==h-1: print(char_frame*w)
    else: print(char_frame+(char_fill*(w-2)+char_frame)*(w>1))

print('#2')
print(char_frame*w+('\n'+(h-2)*(char_frame+(char_fill*(w-2)+char_frame)*(w>1)+'\n')+(char_frame*w))*(h>1))

