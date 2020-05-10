; Code for Program to Calculate power(a,b) i.e a^b in Assembly Language
NAME Comprehensive
TITLE power

ASSUME CS:CODE,DS:DATA
DATA SEGMENT
        BASE DB ?
        POW DB ?
        NL1 DB 0AH,0DH,'ENTER BASE:','$'
        NL2 DB 0AH,0DH,'ENTER POWER:','$'
DATA ENDS

CODE SEGMENT
START:
        MOV AX,DATA
        MOV DS,AX

ENTER_BASE:
        LEA DX,NL1
        MOV AH,09H
        INT 21H

        MOV AH,01H
        INT 21H
        SUB AL,30H
        MOV BL,AL

        MOV BASE,AL

ENTER_POWER:
        LEA DX,NL2
        MOV AH,09H
        INT 21H

        MOV AH,01H
        INT 21H
        SUB AL,30H

        MOV CL,AL
        DEC CL
        MOV AX,00
        MOV AL,BASE

LBL1:
        MUL BL
        LOOP LBL1

        MOV CL,10
        DIV CL
        ADD AX,3030H
        MOV DX,AX

        MOV AH,02H
        INT 21H
        MOV DL,DH
        INT 21H

        MOV AH,4CH
        INT 21H

CODE ENDS
END START
