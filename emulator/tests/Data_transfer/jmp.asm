NAME Data_transfer
TITLE jmp

assume cs:codesg,ds:datasg
; this is add proc ;;

datasg segment
    data1 db 1,02h ,101B,'$   2', 'WoW:),Zp* '
    dw 0123h, 0456H,0abch ,0defh,110101001b
    msg1 DD 1023, 10001001011001011100B,5C2A57F2H
    ARRAY db 10 DUP (1,101b , 'Y') ;?
    mgs2 db 3 dup('hello')
    dw 3 dup(0ffh, 255)
    buff db 'hello world!' ; 65 68 
datasg ends

codesg segment ; for 
        inc ax
 start: mov ax, 0123h;;t;sd 
        mov bx, 0456h
        jmp hr1 
  plc1: jmp near ptr plc2 ;0x10
  plc2: jmp far ptr hr2 ;0x11

  well: add ax, bx
        loop plc2
        
        je well
        ;org 110B
  hr1:  add ax, seg well ;0x15
        JA plc1 
  hr2:  mov bx, offset plc1 ;0x17
        mov ax, buff
        mov cx, buff[SI]
  test:
        mov ax, 4000h
        int 21h

codesg ends
end start;adnfg