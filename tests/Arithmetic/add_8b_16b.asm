NAME Arithmetic
TITLE add_8b_16b
; test passed

ASSUME CS:CODE,DS:DATA

DATA SEGMENT
    num1 DB 05h
    num2 DB 06h
    num3 DW 1234h
    num4 DW 0002h
    sum DB ?
    sum2 DW ?
DATA ENDS  

CODE SEGMENT
    start: mov ax,data
           mov ds,ax           ;initialize data segment
    
           mov al,num1
           add al,num2         ;add the 2 bytes
    
           mov sum,al          ;stores result in memory
    
           mov cx,num3
           add cx,num4         ;add the 2 words
    
           mov sum2,cx         ;stores the result in memory
           out 0,cx

           mov ah,4ch
           int 21h
    
CODE ENDS
END START