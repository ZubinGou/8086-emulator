NAME Arithmetic
TITLE multiply_2_32b
; Test Passed
assume cs:code, ds:data

data segment; data segment starts
    a dw 5678h, 1234h
      dw 5 dup(0)         ;a is 32bit number a=1234 5678
    b dw 1111h, 1111h
      dw 5 dup(0)         ;b is 32bit number b=1111 1111
    c dw 4 dup(?)                       ;reserve 4 words
data ends

code segment
    start:
        mov ax,data
        mov ds,ax
        lea si,a
        lea bx,b
        lea di,c                        ;point to first word
        
        mov ax,word ptr [si]            ;take lower 16bits (5678) of a into ax
        mul word ptr [bx+0]             ;multiply ax with lower 16bits of b(1111) and store in ax
        mov [di],ax                     ;move the contents of ax to c[di]
        mov cx,dx                       ;move the value of dx to cx

        mov ax,word ptr [si+2]          ;take higher 16bits (1234) of a into ax
        mul word ptr [bx+0]             ;multiply ax with lower 16bits of b(1111)and store in ax
        add cx,ax                       ;cx=cx+ax
        mov [di+2],cx                   ;move the contents of cx to c[di+2]
        mov cx,dx                       ;move contents of dx to cx

        mov ax,word ptr [si]            ;take lower 16bits(5678) of a in ax
        mul word ptr [bx+2]             ;multiply contents of ax with higher 16bits of b(1111)
        add word ptr [di+2],ax          ;c[di+2]=c[di+2]+ax
        adc cx,dx                       ;cx=cx+dx+cf
        mov [di+4],ax                   ;move contents of ax to c[di+4]

        mov ax,word ptr [si+2]          ;take higher 16bits of a(1234) into ax
        mul word ptr [bx+2]             ;multiply ax with higher 16bits of b(1111) and store in ax
        add cx,ax                       ;cx=cx+ax
        mov word ptr [di+4],cx          ;move contents of cx to c[di+4]
        adc dx,0000                     ;dx=dx+0000+cf
        mov [di+6],dx                   ;move the contents of dx to c[di+6]

        int 03h                         ;halt
code ends
end start 