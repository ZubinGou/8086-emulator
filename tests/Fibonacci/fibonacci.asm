;Code for Program to Print the Fibonacci series in Assembly Language
.MODEL SMALL

.STACK 64

.DATA
        VAL1    DB      01H
        VAL2    DB      01H
        LP      DB      00H
        V1      DB      00H
        V2      DB      00H
        NL      DB      0DH,0AH,'$'

.CODE

MAIN PROC
        MOV AX,@DATA
        MOV DS,AX

        MOV AH,01H
        INT 21H
        MOV CL,AL
        SUB CL,30H
        SUB CL,2

        MOV AH,02H
        MOV DL,VAL1
        ADD DL,30H
        INT 21H

        MOV AH,09H
        LEA DX,NL
        INT 21H

        MOV AH,02H
        MOV DL,VAL2
        ADD DL,30H
        INT 21H

        MOV AH,09H
        LEA DX,NL
        INT 21H


DISP:
        MOV BL,VAL1
        ADD BL,VAL2

        MOV AH,00H
        MOV AL,BL
        MOV LP,CL
        MOV CL,10
        DIV CL
        MOV CL,LP

        MOV V1,AL
        MOV V2,AH

        MOV DL,V1
        ADD DL,30H
        MOV AH,02H
        INT 21H

        MOV DL,V2
        ADD DL,30H
        MOV AH,02H
        INT 21H

        MOV DL,VAL2
        MOV VAL1,DL
        MOV VAL2,BL

        MOV AH,09H
        LEA DX,NL
        INT 21H


        LOOP DISP

        MOV AH,4CH
        INT 21H

MAIN ENDP
END MAIN
