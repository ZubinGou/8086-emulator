;test most of the rotation instructions
NAME Rotation_and_Shift
TITLE rotation_and_shift

ASSUME CS:CODE

CODE SEGMENT
    START:  MOV AX,FFFFH
            RCL AX
            RCR AX
            ROL AX
            ROR AX
            MOV AX,FFFFH
            SAL AX
            MOV AX,FFFFH
            SAR AX
            MOV AX,FFFFH
            SHL AX
            MOV AX,FFFFH
            SRL AX
            
CODE ENDS
END START
