assume cs:code,ds:data,ss:stack
; 数据段：存储8个字型数据
data segment
    dw 0123h,0456h,0789h,0abch,0defh,0fedh,0cbah,0987h
data ends
; 栈段：定义6个字型数据（共12字节）
stack segment
    dw 0,0,0,0,0,0
stack ends
; 代码段
code segment
start:
    ; 初始化栈段
    mov ax,stack
    mov ss,ax
    mov sp,16  ; 栈顶偏移设为16（栈段大小足够，避免溢出）
    ; 初始化数据段
    mov ax,data
    mov ds,ax
    ; 栈操作：交换data段前两个数据
    push ds:[0]   ; 将data:0的数据压栈
    push ds:[2]   ; 将data:2的数据压栈
    pop ds:[2]    ; 将栈顶数据弹出到data:2
    pop ds:[0]    ; 将栈顶数据弹出到data:0
    ; 程序结束
    mov ax,4c00h
    int 21h
code ends
end start