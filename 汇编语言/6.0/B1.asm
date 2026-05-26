assume cs:codesg, ss:stacksg, ds:datasg

stacksg segment
    dw 0,0,0,0,0,0,0,0
stacksg ends

datasg segment
    db '1. display      '
    db '2. brows        '
    db '3. replace      '
    db '4. modify       '
datasg ends

codesg segment
start:
    ; 初始化数据段寄存器ds
    mov ax, datasg
    mov ds, ax

    ; bx定位行（每个字符串占16字节，共4行）
    mov bx, 0
    mov cx, 4  ; 外层循环：4行
s0:
    ; si定位列（每个单词前4个字母，列索引3~6）
    mov si, 0
    mov dx, 4  ; 内层循环：4列
s:
    ; 取当前字符：ds:[bx+3+si]
    mov al, [bx+3+si]
    ; 小写转大写（ASCII码减20H，a~z→A~Z）
    sub al, 20H
    ; 存回原位置
    mov [bx+3+si], al
    ; 列索引+1
    inc si
    ; 内层循环判断
    dec dx
    jnz s

    ; 行索引+16（下一行）
    add bx, 16
    ; 外层循环判断
    dec cx
    jnz s0

    ; 程序结束
    mov ax, 4C00H
    int 21H
codesg ends

end start