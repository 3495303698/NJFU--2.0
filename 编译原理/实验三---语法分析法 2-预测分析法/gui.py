import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from ll1_parser import LL1Parser

class LL1AnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LL(1) 预测分析器")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        self.root.resizable(True, True)
        
        # 设置全局字体
        default_font = ("Microsoft YaHei", 10)
        text_font = ("Consolas", 10)
        
        # 设置样式
        self.style = ttk.Style()
        self.style.configure("TLabel", font=default_font)
        self.style.configure("TButton", font=default_font, padding=5)
        self.style.configure("TEntry", font=default_font, padding=3)
        
        # 设置表格样式
        self.style.configure("Treeview", font=text_font, rowheight=25)
        self.style.configure("Treeview.Heading", font=default_font, background="#f0f0f0", foreground="#000000", padding=5)
        
        # 设置框架样式
        self.style.configure("TLabelframe", font=("Microsoft YaHei", 11, "bold"))
        
        # 初始化分析器
        self.parser = LL1Parser()
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建左侧框架 - 文法和输入区域
        self.left_frame = ttk.LabelFrame(self.main_frame, text="文法与输入", padding="10")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建右侧框架 - 分析结果区域
        self.right_frame = ttk.LabelFrame(self.main_frame, text="分析过程", padding="10")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧内容 - 文法规则展示
        self.grammar_label = ttk.Label(self.left_frame, text="文法规则:")
        self.grammar_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.grammar_text = scrolledtext.ScrolledText(self.left_frame, width=35, height=12, font=text_font)
        self.grammar_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.grammar_text.config(state=tk.DISABLED, wrap=tk.WORD, bg="#f8f8f8")
        
        # 输入符号串
        input_frame = ttk.Frame(self.left_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.input_label = ttk.Label(input_frame, text="请输入符号串（以#结束）:")
        self.input_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.input_entry = ttk.Entry(input_frame, width=40)
        self.input_entry.pack(fill=tk.X, pady=(0, 5))
        self.input_entry.focus_set()  # 设置焦点到输入框
        
        # 示例提示
        self.example_label = ttk.Label(input_frame, text="示例: i+i# 或 (i*i+i)#", foreground="#666666", font=("Microsoft YaHei", 9))
        self.example_label.pack(anchor=tk.W)
        
        # 按钮区域
        button_frame = ttk.Frame(self.left_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 分析按钮
        self.analyze_button = ttk.Button(button_frame, text="LL(1)分析", command=self.analyze, width=20)
        self.analyze_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 重置按钮
        self.reset_button = ttk.Button(button_frame, text="重置", command=self.reset, width=10)
        self.reset_button.pack(side=tk.LEFT)
        
        # 分析结果
        self.result_label = ttk.Label(self.left_frame, text="分析结果:")
        self.result_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.result_text = scrolledtext.ScrolledText(self.left_frame, width=35, height=4, font=text_font)
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.result_text.config(state=tk.DISABLED, wrap=tk.WORD)
        
        # 退出按钮
        self.exit_button = ttk.Button(self.left_frame, text="退出", command=root.quit, width=30)
        self.exit_button.pack(pady=(0, 5))
        
        # 右侧内容 - 分析过程表格
        # 创建表格框架
        self.tree_frame = ttk.Frame(self.right_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建表格
        columns = ("step", "stack", "input", "production")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", selectmode="extended")
        
        # 定义表头
        self.tree.heading("step", text="步骤", anchor=tk.CENTER)
        self.tree.heading("stack", text="分析栈", anchor=tk.W)
        self.tree.heading("input", text="剩余输入串", anchor=tk.W)
        self.tree.heading("production", text="所用产生式", anchor=tk.W)
        
        # 设置列宽和锚点
        self.tree.column("step", width=60, anchor=tk.CENTER, stretch=False)
        self.tree.column("stack", width=150, anchor=tk.W, minwidth=100)
        self.tree.column("input", width=150, anchor=tk.W, minwidth=100)
        self.tree.column("production", width=200, anchor=tk.W, minwidth=150)
        
        # 添加水平和垂直滚动条
        vscrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hscrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=vscrollbar.set, xscroll=hscrollbar.set)
        
        # 布局表格和滚动条
        vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # 绑定键盘快捷键
        self._bind_keyboard_shortcuts()
        
        # 初始化文法显示
        self._init_grammar_display()
    
    def _bind_keyboard_shortcuts(self):
        """
        绑定键盘快捷键
        """
        # Enter键触发分析
        self.root.bind('<Return>', lambda event: self.analyze())
        # Ctrl+R重置
        self.root.bind('<Control-r>', lambda event: self.reset())
        # Ctrl+Q退出
        self.root.bind('<Control-q>', lambda event: self.root.quit())
        # 设置Tab键在输入框和按钮间循环
        self.input_entry.bind('<Tab>', lambda event: self.analyze_button.focus_set())
        self.analyze_button.bind('<Tab>', lambda event: self.reset_button.focus_set())
        self.reset_button.bind('<Tab>', lambda event: self.exit_button.focus_set())
        self.exit_button.bind('<Tab>', lambda event: self.input_entry.focus_set())
    
    def reset(self):
        """
        重置界面状态
        """
        # 清空输入框
        self.input_entry.delete(0, tk.END)
        # 清空分析结果表格
        for item in self.tree.get_children():
            self.tree.delete(item)
        # 清空结果显示
        self._show_result("", is_error=False)
        # 重新聚焦到输入框
        self.input_entry.focus_set()
    
    def _init_grammar_display(self):
        """
        初始化文法规则的显示
        """
        grammar_str = ""
        grammar_items = [
            "1. E->TG",
            "2. G->+TG|-TG|ε",
            "3. T->FS",
            "4. S->*FS|/FS|ε",
            "5. F->(E)|i"
        ]
        
        for item in grammar_items:
            grammar_str += item + "\n"
        
        self.grammar_text.config(state=tk.NORMAL)
        self.grammar_text.delete(1.0, tk.END)
        self.grammar_text.insert(tk.END, grammar_str)
        self.grammar_text.config(state=tk.DISABLED)
    
    def analyze(self):
        """
        执行LL(1)分析
        """
        # 获取输入字符串
        input_str = self.input_entry.get().strip()
        
        # 验证输入
        if not input_str:
            self._show_result("错误: 请输入符号串", is_error=True)
            # 显示消息框提示
            messagebox.showwarning("输入错误", "请输入符号串进行分析！")
            self.input_entry.focus_set()
            return
        
        # 确保输入以#结尾
        if not input_str.endswith('#'):
            # 提示用户我们添加了#
            original_input = input_str
            input_str += '#'
            # 更新输入框显示
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, input_str)
        
        # 清空之前的分析结果
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # 执行分析
            steps, success, error_msg = self.parser.parse(input_str)
            
            # 显示分析步骤，添加行颜色区分
            for step in steps:
                # 根据步骤类型设置不同的标签颜色
                if step['production'] == "分析成功":
                    self.tree.insert("", tk.END, values=(
                        step['step'],
                        step['stack'],
                        step['input'],
                        step['production']
                    ))
                elif "分析出错" in step['production']:
                    # 对于错误行，可以通过标签设置不同颜色（需要自定义Treeview样式）
                    self.tree.insert("", tk.END, values=(
                        step['step'],
                        step['stack'],
                        step['input'],
                        step['production']
                    ))
                else:
                    self.tree.insert("", tk.END, values=(
                        step['step'],
                        step['stack'],
                        step['input'],
                        step['production']
                    ))
            
            # 滚动到最后一行
            if steps:
                self.tree.see(self.tree.get_children()[-1])
            
            # 显示分析结果
            if success:
                self._show_result(f"{input_str} 为合法符号串", is_error=False)
                # 可选：显示成功消息框
                # messagebox.showinfo("分析成功", f"表达式 '{input_str}' 是合法的！")
            else:
                self._show_result(f"{input_str} 为非法符号串\n错误详情: {error_msg}", is_error=True)
                # 可选：显示错误消息框
                # messagebox.showerror("分析错误", f"表达式 '{input_str}' 是非法的！\n\n错误详情: {error_msg}")
        
        except Exception as e:
            # 捕获所有其他异常
            error_msg = str(e)
            self._show_result(f"程序运行出错: {error_msg}", is_error=True)
            # 显示错误消息框
            messagebox.showerror("程序错误", f"程序运行出错: {error_msg}")
            # 添加错误步骤到表格
            self.tree.insert("", tk.END, values=(
                1,
                "#E",
                input_str,
                f"程序错误: {error_msg}"
            ))
    
    def _show_result(self, result, is_error=False):
        """
        显示分析结果
        :param result: 结果文本
        :param is_error: 是否为错误信息
        """
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        # 根据是否为错误信息设置不同的文本颜色和背景
        if is_error:
            # 创建红色标签和浅色背景
            self.result_text.tag_config("error", foreground="#D8000C", background="#FFD2D2")
            self.result_text.insert(tk.END, result, "error")
            # 设置文本框背景色
            self.result_text.config(bg="#FFD2D2")
        else:
            # 创建绿色标签和浅色背景
            self.result_text.tag_config("success", foreground="#007500", background="#DFF2BF")
            self.result_text.insert(tk.END, result, "success")
            # 设置文本框背景色
            self.result_text.config(bg="#DFF2BF" if result else "#f8f8f8")
        
        self.result_text.config(state=tk.DISABLED)
    
    def _init_grammar_display(self):
        """
        初始化文法规则的显示
        """
        grammar_str = ""
        grammar_items = [
            "1. E->TG",
            "2. G->+TG|-TG|ε",
            "3. T->FS",
            "4. S->*FS|/FS|ε",
            "5. F->(E)|i"
        ]
        
        for item in grammar_items:
            grammar_str += item + "\n"
        
        # 添加使用说明
        grammar_str += "\n使用说明:\n"
        grammar_str += "- 输入表达式必须以#结尾\n"
        grammar_str += "- 支持的运算符: +, -, *, /\n"
        grammar_str += "- 支持括号和标识符i\n"
        grammar_str += "- 示例: i+i# 或 i*(i+i)#"
        
        self.grammar_text.config(state=tk.NORMAL)
        self.grammar_text.delete(1.0, tk.END)
        self.grammar_text.insert(tk.END, grammar_str)
        self.grammar_text.config(state=tk.DISABLED)

# 主程序入口
def main():
    root = tk.Tk()
    app = LL1AnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()