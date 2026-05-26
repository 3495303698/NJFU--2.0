assume cs:code
; a段：16个字型数据（取前8个）
a segment
    dw 1,2,3,4,5,6,7,8,9,0ah,0bh,0ch,0dh,0eh,0fh,0ffh
a ends
; b段：存储逆序结果
b segment
    dw 0,0,0,0,0,0,0,0
b ends
code segment
start:
    ; 初始化a段到ds
    mov ax,a
    mov ds,ax
    ; 初始化b段到es
    mov ax,b
    mov es,ax
    ; 初始化栈段（用a段的剩余空间当栈）
    mov ax,a
    mov ss,ax
    mov sp,32  ; a段共32字节（16个字型），sp设为32表示栈顶在a段末尾
    ; 将a段前8个数据压栈
    mov cx,8
    mov si,0
push_loop:
    push ds:[si]
    add si,2  ; 字型数据占2字节，偏移+2
    loop push_loop
    ; 将栈中数据弹出到b段（逆序）
    mov cx,8
    mov si,0
pop_loop:
    pop es:[si]
    add si,2
    loop pop_loop
    ; 程序结束
    mov ax,4c00h
    int 21h
code ends
end start