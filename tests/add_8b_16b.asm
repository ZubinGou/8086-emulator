data segment
    num1 db 05h
    num2 db 06h
    num3 dw 1234h
    num4 dw 0002h
    sum db ?
    sum2 dw ?
data ends   

assume cs:code,ds:data

code segment
    start: mov ax,data
           mov ds,ax           ;initialize data segment
    
           mov al,num1
           add al,num2         ;add the 2 bytes
    
           mov sum,al          ;stores result in memory
    
           mov cx,num3
           add cx,num4         ;add the 2 words
    
           mov sum2,cx         ;stores the result in memory
    
           mov ah,4ch
           int 21h
    
code ends
end start