NAME String
TITLE display_time

ASSUME CS:CODE, DS:DATA

DATA SEGMENT
    
    MSG1 DB 'Current time is: $'
    HR DB ?
    MIN DB ?
    SEC DB ?
    MSEC DB ?

DATA ENDS

CODE SEGMENT 
    
    START: MOV AX, DATA
    MOV DS, AX

    MOV AH,2CH          ; To get system time
    INT 21H

    MOV HR, CH          ; CH -> Hours
    MOV MIN, CL         ; CL -> Minutes
    MOV SEC, DH         ; DH -> Seconds
    MOV MSEC, DL        ; DL -> 1/100th second

    LEA DX, MSG1        ; Display MSG1
    MOV AH, 09H
    INT 21H

    MOV AL, HR          ; If AL=0D AAM will split the nibbles into AH and AL
    AAM                 ; So AH=01 and AL=03
    MOV BX, AX
    CALL DISPLAY        ; Display hours
    MOV DL, ':'         ; Display ':' after displaying hours
    MOV AH, 02H
    INT 21H
    
    MOV AL, MIN
    AAM
    MOV BX, AX
    CALL DISPLAY        ; Display minutes
    MOV DL, ':'         ; Display ':' after displaying minutes
    MOV AH, 02H
    INT 21H
    
    MOV AL, SEC
    AAM
    MOV BX, AX
    CALL DISPLAY        ; Display seconds
    MOV DL, '.'         ; Display '.' after displaying seconds
    MOV AH, 02H
    INT 21H
    
    MOV AL, MSEC
    AAM
    MOV BX, AX
    CALL DISPLAY        ; Display 1/100th seconds
    MOV AH, 4CH
    INT 21H
    
    DISPLAY:
        MOV DL, BH
        ADD DL, 30H     ; Display BH value
        MOV AH, 02H
        INT 21H
        MOV DL, BL
        ADD DL, 30H     ; Display BL value
        MOV AH, 02H
        INT 21H
        RET
    
CODE ENDS

END START