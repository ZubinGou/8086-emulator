assume cs:codesg,ds:datasg
; this is add proc ;;
codesg segment ; for 

    start:mov ax, 0123h;;t;sd 
    mov bx, 0456h
    org 04h
    well: add ax, bx
    org 110B
    add ax, ax
;aaa
  test:
    mov ax, 4000h
    int 21h

codesg ends

datasg segment
    data1 db 1,02h ,101B,'$   2', 'WoW:),Zp* '
    dw 0123h, 0456H,0abch ,0defh,110101001b
    msg1 DD 1023, 10001001011001011100B,5C2A57F2H
    ARRAY db 10 DUP (1,101b , 'Y') ;?
    mgs2 db 3 dup('hello')
    dw 3 dup(0ffh, 255)
datasg ends

end ;adnfg