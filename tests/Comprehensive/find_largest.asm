;write a program to find the highest among 5 grades.
NAME Arithmetic
TITLE find_largest

assume cs:code, ds:data

data segment
    string1 db 13h,2ch,63h,58h,50h;
data ends
 
code segment
start: mov ax, data
       mov ds, ax         
       mov cx, 04h         ;set up loop counter

       mov bl, 00h         ;bl stores highest grade
       lea si, string1     ;si points to first grade

up:    mov al, [si]        ;compare next grade to highest
       cmp al, bl          
       jl nxt              ;jump if al is still the highest
       mov bl, al          ;else bl holds new highest

nxt:   inc si              ;point to next grade
       dec cx
       jnz up
 
       mov dl,bl
       
code ends
end start