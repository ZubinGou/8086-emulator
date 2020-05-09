ORG 100H            ; set video mode
mov ax,3            ; text mode 80x25, 16 colors, 8 pages(ah=0,al=3)
int 10h             ; interrupt for screen manipulation

mov ax,1003h        ; enable bold background (16 colors) and cancel blinking
mov bx, 0
int 10h

;set segment register
mov ax,0b800h       ; address of VGA card for text mode
mov ds,ax           ; move ax into ds, so ds holds the address of VGA card

;print "Hello World!"
;first byte is ascii code, second byte is color code

mov [02h],'H'

mov [04h],'e'

mov [06h],'l'

mov [08h],'l'

mov [0ah],'o'

mov [0ch],','

mov [0eh],'W'

mov [10h],'o'

mov [12h],'r'

mov [14h],'l'

mov [16h],'d'

mov [18h],'!'


;color all characters
mov cx,12 ; counter register set to number of characters
mov di,03h ; start from byte after 'h'

c: mov [di],11101100b ; light red (1100) on yellow (1110)
   add di,2           ; increment di value by 2 to skip over to next ascii code in VGA memory
   loop c
   
mov ah,0
int 16h ;wait for any key press, keyboard interrupt

ret