;Develop and execute an ALP to compute factorial of a positive integer
;number using recursive procedure.
NAME Comprehensive
TITLE fact

ASSUME CS:CODE,DS:DATA

DATA SEGMENT
    NUM DW 0006H
    FACT DW ?
DATA ENDS

CODE SEGMENT
START:
    mov ax,0
    call s
    inc ax
    mov ax,4c00h
    int 21h
s:  inc ax
    ret

CODE ENDS
END START