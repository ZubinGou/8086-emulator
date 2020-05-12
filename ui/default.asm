NAME Requirement
TITLE bubble_sort

ASSUME CS:CODE,DS:DATA

DATA SEGMENT
    VAL DB 12H,7H,10H,2H,6H
    COUNT DW 5
DATA ENDS

CODE SEGMENT 
    START:
    MOV AX,DATA
    MOV DS,AX 
    
    MOV CX,COUNT       
    DEC CX
       
    NEXTSCAN:
    MOV BX,CX
    MOV SI,0
    NEXTCOMP:
    MOV AL,VAL[SI]
    MOV DL,VAL[SI+1]
    CMP AL,DL
    JC NOSWAP
    MOV VAL[SI],DL
    MOV VAL[SI+1],AL
    NOSWAP:
    INC SI
    DEC BX
    JNZ NEXTCOMP
    LOOP NEXTSCAN
    
    
    print:
          mov cx,count
          xor si,si
    print_again:
        mov al,VAL[si]
      out 0,al
      inc si
            CMP cx,si
      jg print_again
        

    MOV AH,4CH
    INT 21H
CODE ENDS
END START 