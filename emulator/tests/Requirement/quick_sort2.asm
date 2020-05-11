NAME Requirement
TITLE quick_sort

assume cs:code,ds:data

data segment
	dat db 4,8,6,9,2,3,4,7,2,10
	cnt db ?
	l db ?
	r db ?
data ends

code segment
start:
	mov ax,10
	mov cnt,ax
	;call scanf
	;初始化l,r
	mov ax,0
	mov l,ax;
	mov ax,9
	mov r,ax
	;调用快排
	call quicksort
	call print

;封装交换函数
swap:
	;利用xchg 可以少用一个寄存器来充当临时变量
	mov dx,dat[si];
	xchg dx,dat[bx];
	xchg dx,dat[si];
	ret
 
quicksort:
	mov ax,l
	cmp ax,r
	jg over
	xor si,si;
	xor bx,bx;
	mov si,l;i
	mov bx,r;j
	mov ax,dat[si] 
	sort_again:
	cmp bx,si;				while (i!=j)
	je over_loop;
		loop_j_again:
			cmp si,bx; 			while(i<j)
			jge over_loop
			cmp ax,dat[bx]; 	while (a[j]>=a[l])
			jg loop_i_again
			add bx ,-1			;		j--
			jmp loop_j_again;	
		loop_i_again:
			cmp si,bx; 			while (i<j)
			jge over_loop
			cmp ax,dat[si]; 	while (a[l]>=a[i])
			jl compare;
			add si,1;					i++
			jmp loop_i_again;
		compare:
			cmp si,bx;			if (i>=j)
			jge over_loop;				break
			call swap;				swap(i,j)
	jmp sort_again
	over_loop:
		mov bx,l;
		call swap;				swap(i,l)
		push si; push i
		push r  ;push r
		mov r,si
		add r ,-1
		call quicksort;			quicksort(l,i-1);
		pop r
		pop bx
		mov l,bx;
		inc l
		call quicksort;			quicksort(i+1,r);
	over:
		ret

 
;封装一个输出函数
print:
	mov cx,cnt
	xor si,si
    print_again:
			mov ax,dat[si]
			out 0,ax
			inc si;
			loop print_again
	MOV AH,4CH
    INT 21H

code ends
end start