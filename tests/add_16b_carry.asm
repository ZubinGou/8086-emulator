data segment
    var1 dw 1234h
    var2 dw 5140h
    result dw ?
    carry db 00h
data ends

code segment
    
    assume cs:code,ds:data
    
    mov ax,data
    mov ds,ax
   
start: mov ax,var1
       add ax,var2
       jnc skip
       mov carry,01h

skip: mov result,ax

      int 03h

end start
code ends
end