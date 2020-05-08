;ALP to copy the string of successive memory locations from one memory to
;other
;Using string instructions


DATA SEGMENT
    SOURCE DB "BIOMEDICAL"
DATA ENDS

EXTRA SEGMENT
    DEST DB ?
EXTRA ENDS

CODE SEGMENT
    ASSUME CS:CODE , DS:DATA, ES:EXTRA
    START : MOV AX,DATA
            MOV DS,AX
            MOV AX,EXTRA
            MOV ES,AX
            MOV SI,00H
            MOV DI,00H
            CLD
            MOV CX,000AH
            REP MOVSB
            
         X: MOV AL,SOURCE [SI]
            MOV DEST [DI],AL
            INC SI
            INC DI
            LOOP X
            
            MOV AH,4CH
            INT 21H
CODE ENDS
END START