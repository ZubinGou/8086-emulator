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
	mov al,10
	mov cnt,al
	;call scanf
	;初始化l,r
	mov al,0
	mov l,al;
	mov al,9
	mov r,al
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
	mov al,l
	cmp al,r
	jg over
	xor si,si;
	xor bx,bx;
	mov si,l;i
	mov bx,r;j
	mov al,dat[si] 
	sort_again:
	cmp bx,si;				while (i!=j)
	je over_loop;
		loop_j_again:
			cmp si,bx; 			while(i<j)
			jge over_loop
			cmp al,dat[bx]; 	while (a[j]>=a[l])
			jg loop_i_again
			add bx ,-1			;		j--
			jmp loop_j_again;	
		loop_i_again:
			cmp si,bx; 			while (i<j)
			jge over_loop
			cmp al,dat[si]; 	while (a[l]>=a[i])
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
			mov al,dat[si]
			out 0,al
			inc si;
			loop print_again
	ret

code ends
end start