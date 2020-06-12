;program to subtract two 8b numbers
NAME Arithmetic
TITLE sub_8b
; Test Passed
assume cs:code,ds:data
data segment
    num1 db ?
    num2 db ?
    res db ?
    msg1 db 10,13,"enter the first number: $"
    msg2 db 10,13,"enter the second number: $"
    msg3 db 10,13,"result of subtraction is: $"
data ends   


code segment
    start: mov ax,data
           mov ds,ax           ;initialize data segment 
           
           lea dx,msg1         ;load address of msg1 into dx
           mov ah,9h           ;interrupt to display contents of dx
           int 21h    
           
           mov ah,1h           ;read a character from console
           int 21h
           sub al,30h          ;convert number into bcd from ascii form
           mov num1,al         ;store number as num1
           
           lea dx,msg2         ;load address of msg2 into dx
           mov ah,9h           ;interrupt to display contents of dx
           int 21h    
           
           mov ah,1h           ;read a character from console
           int 21h
           sub al,30h          ;convert number into bcd from ascii form
           mov num2,al         ;store number as num2
           
           mov al,num1         
           sub al,num2         ;sub num2 from num1
           mov res,al          ;store sum in res
           mov ah,0            ;clear garabage value (ah to be used later)
           aaa                 ;converts hex to bcd and stores values in ah and al 
           add ah,30h          ;first digit converted into bcd
           add al,30h          ;second digit converted from ascii to bcd
           
           mov bx,ax           ;save value of ax into bx
           lea dx,msg3         ;print ms3
           mov ah,9h
           int 21h
           
           mov ah,2h           ;print first digit
           mov dl,bh                                
           int 21h
           
           mov ah,2            ;print second digit
           mov dl,bl
           int 21h
    
           mov ah,4ch
           int 21h
    
code ends
end start