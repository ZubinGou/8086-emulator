NAME Interrupt
TITLE show_date_time
; Using DOS Interrupt to get system date and time

ASSUME CS:CODE,DS:DATA

DATA SEGMENT
PROMPT1    DB  'Current System Date is : $'
DATE       DB  '0000-00-00$'  ; date format year:month:day
PROMPT2    DB  'Current System Time is : $'     
TIME       DB  '00:00:00$'    ; time format hr:min:sec
DATA ENDS

CODE SEGMENT
    MAIN:
        MOV AX, DATA          ; initialize DS
        MOV DS, AX
        ;-------------Print DATE-------------------------
        LEA BX, DATE          ; BX=offset of string DATE
        CALL GET_DATE         ; call the procedure GET_DATE

        LEA DX, PROMPT1       ; DX=offset of string PROMPT
        MOV AH, 09H           ; print the string PROMPT
        INT 21H                      

        LEA DX, DATE          ; DX=offset of string TIME
        MOV AH, 09H           ; print the string TIME
        INT 21H     
        ;-------------Print TIME-------------------------
        LEA BX, TIME          ; BX=offset of string TIME
        CALL GET_TIME         ; call the procedure GET_TIME

        LEA DX, PROMPT2       ; DX=offset of string PROMPT
        MOV AH, 09H           ; print the string PROMPT
        INT 21H                      

        LEA DX, TIME          ; DX=offset of string TIME
        MOV AH, 09H           ; print the string TIME
        INT 21H                      

        MOV AH, 4CH           ; return control to DOS
        INT 21H

    ;*************************************************************;
    ;-----------------------  GET_TIME  --------------------------;
    ;*************************************************************;
    GET_TIME:
        ; this procedure will get the current system time 
        ; input : BX=offset  of the string TIME
        ; output : BX=current time
        PUSH AX         ; PUSH AX onto the STACK
        PUSH CX         ; PUSH CX onto the STACK 

        MOV AH, 2CH     ; get the current system time
        INT 21H                       

        MOV AL, CH      ; set AL=CH , CH=hours
        CALL CONVERT    ; call the procedure CONVERT
        MOV [BX], AX    ; set [BX]=hr

        MOV AL, CL      ; set AL=CL , CL=minutes
        CALL CONVERT    ; call the procedure CONVERT
        MOV [BX+3], AX  ; set [BX+3]=min
                                                
        MOV AL, DH      ; set AL=DH , DH=seconds
        CALL CONVERT    ; call the procedure CONVERT
        MOV [BX+6], AX  ; set [BX+6]=sec
                                                            
        POP CX          ; POP a value from STACK into CX
        POP AX          ; POP a value from STACK into AX

        RET             ; return control to the calling procedure

    ;*************************************************************;
    ;-----------------------  GET_DATE  --------------------------;
    ;*************************************************************;

    GET_DATE:
    ; this procedure will get the current system time 
    ; input : BX=offset  of the string TIME
    ; output : BX=current time
        PUSH AX                ; PUSH AX onto the STACK
        PUSH CX                ; PUSH CX onto the STACK 

        MOV AH, 2AH            ; get the current system Date
        INT 21H                       

        PUSH BX
        MOV BL, 100
        MOV AX,CX
        DIV BL
        MOV CX,AX
        POP BX

        MOV AL, CH             ; set AL=CH , CH=Year
        CALL CONVERT           ; call the procedure CONVERT
        MOV [BX], AX           ; set [BX]=Year

        MOV AL, CL             ; set AL=CL , CL=Year
        CALL CONVERT           ; call the procedure CONVERT
        MOV [BX+2], AX         ; set [BX+2]=Year
                                                
        MOV AL, DH             ; set AL=DH , DH=Month
        CALL CONVERT           ; call the procedure CONVERT
        MOV [BX+5], AX         ; set [BX+5]=Month
                                                            
        MOV AL, DL             ; set AL=DH , DH=Day
        CALL CONVERT           ; call the procedure CONVERT
        MOV [BX+8], AX         ; set [BX+8]=Day

        POP CX                 ; POP a value from STACK into CX
        POP AX                 ; POP a value from STACK into AX
        RET                    ; return control to the calling procedure
        
    ;*************************************************************;
    ;------------------------  CONVERT  --------------------------;
    ;*************************************************************;

    CONVERT:
    ; this procedure will convert the given binary code into ASCII code
    ; input : AL=binary code
    ; output : AX=ASCII code
        PUSH DX                ; PUSH DX onto the STACK 
        MOV AH, 0              ; set AH=0
        MOV DL, 10             ; set DL=10
        DIV DL                 ; set AX=AX/DL
        OR AX, 3030H           ; convert the binary code in AX into ASCII
        POP DX                 ; POP a value from STACK into DX 
        RET                    ; return control to the calling procedure

CODE ENDS
END MAIN
