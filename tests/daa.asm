.model small
.stack 200
.data
num1 db	27h
num2 db	35h	

.code
.startup
	mov	al, num1	;load ax with number num1
	add al, num2	;al = al + num2 i.e. al = 5ch = 92 in decimal
	;the expected result is 62 in decimal
	daa				; al = 62
.exit
end