
ASSUME CS:CODE,DS:DATA

DATA SEGMENT
    msg db 'Hello! Welcome to 8086-emulator!!!$'
    num2 DB 06h
    num3 DW 1234h
    num4 DW 0002h
    sum DB ?
    sum2 DW ?
DATA ENDS  

CODE SEGMENT
    start: 
        mov ax,data
        mov ds,ax          ;initialize data segment

        mov dx,offset msg  ;lea dx,msg
        mov ah,9 
        int 21h            ; print msg

        mov ah,4ch
        int 21h  
    
CODE ENDS
END START



