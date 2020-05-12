;# 8086 Program to check the given no for Prime   #

;NUM is assigned to the Number to be checked
;AL is used as the default no
;BL is used as Dividing Variable. It is Incremented in each loop
;BH is used to know the number of variables which can divide the Number. BH>02, The number is not prime
;BL is made to run x number of times, where x is the given number.
NAME Comprehensive
TITLE given_number_prime
;text passed
; Declaration Part
ASSUME CS:CODE,DS:DATA

DATA SEGMENT
    MSG DB "The Give No is a Prime No$"
    NMSG DB "The Given No is not a Prime No$"
    NUM DB 71H      ;Enter the required no here
DATA ENDS

CODE SEGMENT
    START:  MOV AX,DATA
            MOV DS,AX

            MOV AL,NUM
            MOV BL,02H      ; The Dividing starts from 2, Hence BH is compare to 02H
            MOV DX,0000H    ; To avoid Divide overflow error
            MOV AH,00H      ; To avoid Divide overflow error

    ;Loop to check for Prime No
    L1:     DIV BL
            CMP AH,00H      ; Remainder is compared with 00H (AH)
            JNE NEXT
            INC BH          ; BH is incremented if the Number is divisible by current value of BL
    NEXT:   CMP BH,02H ; If BH > 02H, There is no need to proceed, It is not a Prime
            JE FALSE        ; The no is not a Prime No
            INC BL          ; Increment BL
            MOV AX,0000H    ; To avoid Divide overflow error
            MOV DX,0000H    ; To avoid Divide overflow error
            MOV AL,NUM      ; Move the Default no to AL
            CMP BL,NUM      ; Run the loop until BL matches Number. I.e, Run loop x no of times, where x is the Number given
            JNE L1          ; Jump to check again with incremented value of BL

    ;To display The given no is a Prime No
    TRUE:   LEA DX,MSG
            MOV AH,09H      ; Used to print a string
            INT 21H
            JMP EXIT

    ;To display The given no is not a Prime No
    FALSE:  LEA DX,NMSG
            MOV AH,09H      ; Used to print a string
            INT 21H


    EXIT:
            MOV AH,4CH
            INT 21H
CODE ENDS
END START
