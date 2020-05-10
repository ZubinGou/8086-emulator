;Develop and execute ALP that implements Binary search algorithm. The data
;consists of sorted 16 bit unsigned integers. The search key is also a 16 bit unsigned
;integer.
NAME Searching
TITLE binary_search

ASSUME CS:CODE,DS:DATA

DATA SEGMENT
    ARR DW 05H,0111H,2161H,4541H,7161H,8231H
    SR EQU 4541H
    MSG1 DB 'ELEMENT FOUND AT '
    RES DB ' RD POSITION','$'
    MSG2 DB 'ELEMENT NOT FOUND','$'
DATA ENDS


CODE SEGMENT
    START:  MOV AX,DATA
            MOV DS,AX
            MOV BX,00H
            MOV CX,SR
            MOV DX,05H

    LP: CMP BX,DX
        JA FAILURE
        MOV AX,BX
        ADD AX,DX
        SHR AX,01
        MOV SI,AX
        ADD SI,SI
        CMP CX,ARR[SI]
        JAE BIGGER
        DEC AX
        MOV DX,AX
        JMP LP  
    
BIGGER: JE SUCCESS
        INC AX
        MOV BX,AX
        JMP LP
        
SUCCESS:ADD AL,01H
        ADD AL,2FH
        MOV RES,AL
        LEA DX,MSG1
        JMP DISPLAY
        
FAILURE: LEA DX,MSG2
DISPLAY: MOV AH,09H
         INT 21H
         MOV AH,4CH
         INT 21H      
         
CODE ENDS
END START