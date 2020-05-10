assume cs:codesg

codesg segment
        org 100h
 start: mov al,var1         ;check value of var1 by moving it to al
        lea bx,var1         ;get address of var1 in bx
        mov cs:[bx],44h      ;check value of var1 by moving it to al
        ret
        var1 db 22h
ends codesg 
end start