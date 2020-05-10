NAME Inout
TITLE inout

assume cs:codesg,ds:datasg
; this is add proc ;;
codesg segment ; for 
start:
    mov ax,0x1234
    inc ax
    out 4, al
    out 10h, ax
    mov dx,1088
    out dx,ax
    in ax, 101
    in al,0
    out dx, ah
    jmp finish
    buff db 'hello world! XD'
finish:
    mov ax, $
    int 21h

codesg ends

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

end start