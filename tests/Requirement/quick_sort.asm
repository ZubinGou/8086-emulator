NAME Requirement
TITLE quick_sort

assume cs:code,ds:data

data segment
	dat dd 4,8,6,9,2,3,4,7,2,10
	cnt dd ?
	l dd ?
	r dd ?
data ends

code segment
start:
	mov eax,10
	mov cnt,eax
	call scanf
	;初始化l,r
	mov eax,0
	mov l,eax;
	mov eax,9
	mov r,eax
	;调用快排
	call quicksort
	call print
	exit
;封装交换函数
swap:
	;利用xchg 可以少用一个寄存器来充当临时变量
	mov edx,dat[esi*4];
	xchg edx,dat[ebx*4];
	xchg edx,dat[esi*4];
	ret
 
quicksort:
	mov eax,l
	cmp eax,r
	jg over
	xor esi,esi;
	xor ebx,ebx;
	mov esi,l;i
	mov ebx,r;j
	mov eax,dat[esi*4] 
	sort_again:
	cmp ebx,esi;				while (i!=j)
	je over_loop;
		loop_j_again:
			cmp esi,ebx; 			while(i<j)
			jge over_loop
			cmp eax,dat[ebx*4]; 	while (a[j]>=a[l])
			jg loop_i_again
			add ebx ,-1			;		j--
			jmp loop_j_again;	
		loop_i_again:
			cmp esi,ebx; 			while (i<j)
			jge over_loop
			cmp eax,dat[esi*4]; 	while (a[l]>=a[i])
			jl compare;
			add esi,1;					i++
			jmp loop_i_again;
		compare:
			cmp esi,ebx;			if (i>=j)
			jge over_loop;				break
			call swap;				swap(i,j)
	jmp sort_again
	over_loop:
		mov ebx,l;
		call swap;				swap(i,l)
		push esi; push i
		push r  ;push r
		mov r,esi
		add r ,-1
		call quicksort;			quicksort(l,i-1);
		pop r
		pop ebx
		mov l,ebx;
		inc l
		call quicksort;			quicksort(i+1,r);
	over:
		ret

 
;封装一个输出函数
print:
	mov ecx,cnt
	xor esi,esi
    print_again:
			mov eax,dat[esi*4]
			call writeint
			call crlf
			inc esi;
			loop print_again
	ret

code ends
end start