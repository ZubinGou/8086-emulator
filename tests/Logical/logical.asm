;test most of the logical instructions
NAME Logical
TITLE logical

ASSUME CS:CODE

CODE SEGMENT
    START:  MOV AX,0505H
            MOV BX,C0C0H
            MOV CX,1122H
            AND AX,BX
            OR AX,BX
            XOR AX,BX
            NOT CX
            NEG AX
            CMP AX,1000H
            TEST AX,BX
CODE ENDS
END START
