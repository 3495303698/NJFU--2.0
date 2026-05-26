import tkinter as tk
from gui import LL1AnalyzerGUI

if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    # 创建并显示GUI
    app = LL1AnalyzerGUI(root)
    # 启动主事件循环
    root.mainloop()