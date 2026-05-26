assume cs:code
code segment
    mov ax,0
    mov ds,ax       ; DS指向0段
    mov bx,200h     ; 起始偏移地址0:200
    mov cx,40h      ; 循环64次（0~63）
    mov al,0        ; 初始数据0
s:  mov [bx],al     ; 写入内存
    inc al
    inc bx
    loop s
    mov ax,4c00h
    int 21h
code ends
end