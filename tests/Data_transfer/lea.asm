NAME Data_transfer
TITLE lea

assume cs:codesg,ds:datasg

datasg segment
        var1 db 22h
datasg ends

codesg segment
        org 100h
 start: mov al,var1         ;check value of var1 by moving it to al
        lea bx,var1         ;get address of var1 in bx 
        mov cs:[bx],44h      ;check value of var1 by moving it to al
        lds ax,[bx]
        les ax,[bx]
        xchg ax,bx
        ret
codesg ends 
end start