assume cs:code
; a段：8个字节数据
a segment
    db 1,2,3,4,5,6,7,8
a ends
; b段：8个字节数据
b segment
    db 1,2,3,4,5,6,7,8
b ends
; c段：存储相加结果
c segment
    db 0,0,0,0,0,0,0,0
c ends
code segment
start:
    ; 初始化a段地址到ds
    mov ax,a
    mov ds,ax
    ; 初始化b段地址到es
    mov ax,b
    mov es,ax
    ; 初始化c段地址到bx
    mov ax,c
    mov bx,ax
    ; 循环8次，依次相加
    mov cx,8
    mov si,0  ; 偏移地址初始化为0
s:
    mov al,ds:[si]   ; 取a段的一个字节
    add al,es:[si]   ; 加上b段的对应字节
    mov [bx+si],al   ; 结果存到c段的对应位置
    inc si           ; 偏移地址+1
    loop s           ; 循环直到cx=0
    ; 程序结束
    mov ax,4c00h
    int 21h
code ends
end start