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

    dw 0123h,0456h,0789h,0abch,0defh

datasg ends

end ;adnfg