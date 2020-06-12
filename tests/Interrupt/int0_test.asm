
ASSUME CS:CODE,DS:DATA

DATA SEGMENT
    msg db 'Hello! This is int0_test!$'
DATA ENDS  

CODE SEGMENT
    start: 
        mov ax, 1000h
        mov bl, 0     
        div bl      ; 寄存器AX中的值除以寄存器BL中的值，结果中商存入AL，余数存入AH

        mov ah,4ch
        int 21h  
    
CODE ENDS
END START