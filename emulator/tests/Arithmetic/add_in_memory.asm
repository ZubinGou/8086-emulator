;add a series of 10 bytes stores in the memory from locs
;20,000H to 20,009. Store the result immediately after the series.
NAME Arithmetic
TITLE add_in_memory
; Test Passed
assume cs:code,ds:data

DATA SEGMENT
        a db 3 dup(9,11h,101b,0xa1)
DATA ENDS


CODE SEGMENT
    
start:  mov ax,2000H
        mov ds,ax
    
        mov si,0000H    ;starting offset address = 0000H
        mov cx,000AH    ;10 bytes = 'A'
        mov ax,0000H    ;ax initialized to store sum
    
back:   add al,[si]     ;indirect register addressing
        jnc skip        ;jump if no carry
        inc ah          ;if sum is greater than 8 bit
skip:   inc si          ;point to next offset
        loop back       ;decrement cx by 1
        
        mov [si],ax     ;store final result in 20,009H
        out 0,ax
        HLT 
CODE ENDS    
END START                                           