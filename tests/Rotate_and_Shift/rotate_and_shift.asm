;test most of the rotation instructions
NAME Rotation_and_Shift
TITLE rotation_and_shift

ASSUME CS:CODE

CODE SEGMENT
    START:  MOV AX,FFFFH
            RCL AX,1
            RCL AX,1
            RCR AX,2
            ROL AX,2
            ROR AX,2
            SAL AX,2
            SAR AX,2
            SHL AX,2
            SHR AX,2
            
CODE ENDS
END START
