NAME String
TITLE display_string

assume cs:code,ds:data

data segment
    message db "Hello World This is a test $"
data ends

code segment
start: mov ax,data
       mov ds,ax
       mov ah,09h
       lea dx,message
       out 0,dx
       int 21h

       mov ax,4c00h
       int 21h

code ends
end start