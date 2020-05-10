;test most of the stack instructions
NAME Stack
TITLE stack

ASSUME CS:CODE

CODE SEGMENT
    START:  MOV AX,FFFFH
            MOV BX,C0C0H
            MOV CX,1122H
            PUSH AX
            PUSH BX
            PUSH CX
            POP AX
            POP BX
            POP CX
CODE ENDS
END START
