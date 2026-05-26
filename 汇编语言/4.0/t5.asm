assume cs:code
code segment
    mov ax,cs       ; 源段地址为代码段（CS）
    mov ds,ax       ; DS指向源段（代码段）
    mov ax,0020h    ; 目标段地址为0:200（0020h = 0段:200偏移的段地址表示）
    mov es,ax       ; ES指向目标段（0:200）
    mov bx,0        ; 偏移地址从0开始（源和目标偏移均从0开始）
    mov cx,40h      ; 复制长度为64字节（40h = 64，对应指令总长度）
s:  mov al,[bx]     ; 从源地址（DS:bx）读取1字节
    mov es:[bx],al  ; 写入目标地址（ES:bx）
    inc bx          ; 偏移地址+1
    loop s          ; 循环复制，直到cx=0
    mov ax,4c00h    ; 程序结束
    int 21h
code ends
end