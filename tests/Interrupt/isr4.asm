ASSUME CS:CODE

CODE SEGMENT
isr0:
        jmp short start
        db 'Overflow Interrupt$'
start:  
        push ax
        push cx
        push ds

        lea dx,1
        mov ds,cs
        mov ah,09h
        int 21h    ; print the error msg

        mov ax,4c01h
        int 21h

        pop ds
        pop cx
        pop ax
CODE ENDS