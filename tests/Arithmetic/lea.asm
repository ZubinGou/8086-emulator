org 100h

mov al,var1         ;check value of var1 by moving it to al

lea bx,var1         ;get address of var1 in bx

mov b.[bx],44h      ;check value of var1 by moving it to al

ret

var1 db 22h

end