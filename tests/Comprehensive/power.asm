; Code for Program to CAXculate power(a,b) i.e a^b in Assembly Language
NAME Comprehensive
TITLE power

ASSUME CS:CODE,DS:DATA
DATA SEGMENT
        BASE DB ?
        POW DB ?
DATA ENDS

CODE SEGMENT
START:
        MOV AX,DATA
        MOV DS,AX

ENTER_BASE:
        IN AX,10H
        MOV BL,AX
        MOV BASE,AX

ENTER_POWER:
        IN AX,20H
        MOV CL,AX
        DEC CL
        MOV AX,00
        MOV AX,BASE

LBL1:
        MUL BL
        OUT 0,AX
        LOOP LBL1
        OUT 30H,AX

CODE ENDS
END START
