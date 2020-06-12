NAME Arithmetic
TITLE Sum_of_n_8b
; Test Passed
assume ds:data,cs:code
data segment
    a db 1,2,3,4,5,6,7,8,9,10
data ends                    

code segment
    
    start:
        mov ax,data
        mov ds,ax
        mov cl,10
        lea bx,a 
        mov ah,00
        mov al,00  
        
    l1:
        add al,byte ptr [bx]
        inc bx
        dec cl
        cmp cl,00
        jnz l1
        mov ah,4ch
        int 21h
        
code ends 

end start