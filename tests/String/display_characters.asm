NAME String
TITLE display_characters

assume cs:code

code segment
    start: mov dl,'a'        ;store ascii code of 'a' in dl
           out 0,dl
           mov ah,2h         ;ms-dos character output function
           int 21h           ;displays character in dl register
           
           mov ax,4c00h      ;return to ms-dos
           int 21h           ;do it!
code ends
end start