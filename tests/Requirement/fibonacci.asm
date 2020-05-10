;Code for Program to Print the Fibonacci series in Assembly Language
NAME Requirement
TITLE fibonacci

ASSUME CS:CODE,DS:DATA

;Declaration Part
DATA SEGMENT
        RES DB ?
        CNT DB 0AH       ; Initialize the counter for the no of Fibonacci No needed
DATA ENDS

CODE SEGMENT
        START: MOV AX,DATA
               MOV DS,AX
               LEA SI,RES
               MOV CL,CNT       ; Load the count value for CL for looping
               MOV AX,00H       ; Default No
               MOV BX,01H       ; Default No

               ;Fibonacci Part
               L1:ADD AX,BX
               MOV [SI],AX
               MOV AX,BX
               MOV BX,[SI]
               INC SI
               OUT 0,BX
               LOOP L1

               INT 3H           ; Terminate the Program
CODE ENDS
END START
