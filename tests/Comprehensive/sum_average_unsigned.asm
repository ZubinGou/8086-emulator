;ALP to find the Sum and average of unsigned integer.
NAME Comprehensive
TITLE sum_average_unsigned
;test passed

ASSUME CS:CODE,DS:DATA

DATA SEGMENT
    A DW 1234H,3223H,0FFFFH,4326H,0FEF3H,4325H
    N DW 0006H
    SUM DW 2 DUP(0)
    AVG DW ?
DATA ENDS


CODE SEGMENT

START: MOV AX,DATA
       MOV DS,AX
       MOV SI,0000H
       MOV DX,0000H
       MOV CX,N
       MOV AX,0000H
       CLC

X:     ADD AX,A[SI]
       JC K

X1:    INC SI
       INC SI
       LOOP X
       JMP QUIT
       
K:     ADD DX,0001H
       JMP X1

QUIT:  MOV SUM,AX
       MOV SUM+2,DX
       DIV N
       MOV AVG,AX
       OUT 0,AX
       MOV AH,4CH
       INT 21H  
       
CODE ENDS
END START