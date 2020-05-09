; Hello world!

data segment
    msg db "Hello,World!$"
data ends
    
code segment
    assume cs:code,ds:data
    start: mov ax,data          ;intialize DS to address
           mov ds,ax            ;of data segment
           lea dx,msg           ;load effect address of message
           
           mov ah,09h           ;display string function
           int 21h              ;display message
           
    exit:  mov ax,4c00h         ;DOS function: Exit program
           int 21h              ;Call DOS, terminate program
code ends
end start