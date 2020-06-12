assume cs:code,ds:data

data segment
    msg db 'helloworld'
data ends

code segment
    start: mov ax,data
           mov ds,ax

           mov si,0           ;call upper int
           int 7ch
           
           mov dx,offset msg  ;lea dx,msg
           mov ah,9 
           int 21h            ; using dos interrupt to print msg

           mov ax,4c00h
           int 21h
code ends
end start








