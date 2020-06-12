;find out largest number from an unordered array of sixteen 8-bit 
;numbers stored sequentially in memory location 2000:5000H. Store 
;the largest number in memory location 2000:5000H
NAME Comprehensive
TITLE finding_largest_number_memory

assume cs:code, ds:data

data segment
    A DB 13h,2ch,63h,58h,50h,10h,17h,89h,91h,00h,02h,53h,68h,18h,47h,18h;
data ends
 
code segment
    
start:  mov ax,data
        mov ds,ax
        
        lea bx,A                ;si points to first number
        mov di,5000H            ;starting offset address = 5000H
        mov cx,0010H            ;16 bytes of data
        mov dx,0000H            ;dx initialized to store numbers
    
back:   mov dl,byte ptr [bx]     ;transfer string to al ;0x6
        
        mov ax,2000H            ;change segment
        mov ds,ax
        
        mov [di],dl             ;transfer string to di
        
        mov ax,data             ;change segment
        mov ds,ax

        inc bx                  ;point to next byte
        inc di                  ;point to next memory address
        loop back               ;decrement cx by 1

        mov ax,2000H            ;change segment
        mov ds,ax
        
;--------------clearing registers-------------------------------

        xor cx,cx
        xor bx,bx  
        xor si,si                      
       
;--------------find largest-------------------------------------
       
        mov cx, 10h              ;set up loop counter

        mov bl, 00h              ;bl stores highest number
        mov si, 5000H            ;si points to first number

up:     mov al,byte ptr [SI]      ;compare next number to highest
        cmp al, bl               
        jl nxt                   ;jump if al is still the highest
        mov bl, al               ;else bl holds new highest

nxt:    inc si                   ;point to next number
        dec cx
        jnz up
        
        mov dl,bl
        
        mov [si+1],bl            ;store highest number
        hlt                
       
code ends
end start