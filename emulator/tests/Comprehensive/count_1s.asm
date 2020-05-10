;program to count number of binary 1s
NAME Arithmetic
TITLE count_1s

assume cs:code,ds:data
data segment
    data1 db ? 
    msg1 db 10,13,"enter the number: $"
    msg3 db 10,13,"number of 1s are: $"
data ends   
 
code segment
start: mov ax,data
       mov ds,ax
       sub bl,bl
       
       lea dx,msg1         ;load address of msg1 into dx
       mov ah,9h           ;interrupt to display contents of dx
       int 21h
       
       mov ah,1h           ;read a character from console
       int 21h
       sub al,30h          ;converting from ascii into bcd form
       
       mov dl,8h           ;set up count register
again: rol al,1
       jnc next            ;conditional jump if carry flag is 0
       inc bl              ;number of 1s
 next: dec dl
       jnz again           ;short jump if del is not zero
       
       lea dx,msg3         ;print msg3
       mov ah,9h
       int 21h
           
       mov ah,2h           ;print number of 1s
       add bl,30h
       mov dl,bl                                
       int 21h
       
exit: mov ah,04ch
      mov al,0
      int 21h 
      
code ends
end start