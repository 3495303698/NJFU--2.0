assume cs:code
code segment
    mov ax,0200h    ; 1. 将ES段寄存器指向0:200（0200h = 0段:200偏移）
    mov es,ax       ; 2. 完成ES初始化
    mov bx,0        ; 3. 偏移地址从0开始（ES:bx即0:200+0）
    mov al,0        ; 4. 初始数据为0
    mov cx,40h      ; 5. 循环64次（40h = 64）
s:  mov es:[bx],al  ; 6. 向目标内存写入数据
    inc al          ; 7. 数据+1（0→1→...→63）
    inc bx          ; 8. 偏移地址+1（指向下一个内存单元）
    loop s          ; 9. 循环（直到cx=0）
    mov ax,4c00h    ; 10. 程序结束
    int 21h         ; 11. 调用中断结束程序
code ends
end