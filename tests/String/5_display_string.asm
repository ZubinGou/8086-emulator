data segment
    message db "Hello World This is a test $"
data ends

code segment
    assume cs:code,ds:data
start: mov ax,data
       mov ds,ax
       mov ah,09h
       lea dx,message
       int 21h

       mov ax,4c00h
       int 21h

code ends
end start