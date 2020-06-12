NAME Data_transfer
TITLE address

assume cs:codesg,ds:datasg

datasg segment
    data1 db 1,0ffh ,101B,'$   2', 'WoW:),Zp* '
    dw 0123h, 0456H,0abch ,0defh,110101001b
    msg1 DD 1023, 10001001011001011100B,5C2A57F2H
    ARRAY db 2 DUP (1,101b , 'Y') ;?
    mgs2 db 3 dup('hello')
    db ?
    db 3 dup(0ffh, 25)
    dw 3 dup(?) 
datasg ends

codesg segment ; for 
start:      mov bx, 10
            mov ah, [200+bx]
            mov ax, 200[bx]
            mov ax, [bx].200
            mov ax, 0x2000[bx]
            mov ax, 200[bx][si]
            mov ax,[bx].200[si]
            mov ax,[bx][si][.200]
            mov ds:[40H],ax
            mov ax,es:[bx]
;aaa
test:
        mov ax, $
        int 21h

codesg ends
end start;adnfg