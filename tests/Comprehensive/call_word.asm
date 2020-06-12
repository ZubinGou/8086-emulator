;Develop and execute an ALP to compute factorial of a positive integer
;number using recursive procedure.
NAME Comprehensive
TITLE fact

ASSUME CS:CODE, SS:stack

stack SEGMENT
    dw 8 dup (0)
stack ENDS

CODE SEGMENT
START:
    mov ax,stack
    mov ss,ax
    mov sp,16
    mov ds,ax
    mov ax,0
    call word ptr ds:[0EH]
    inc ax
    inc ax
    inc ax
    mov ax,4c00h
    int 21h
CODE ENDS
END START