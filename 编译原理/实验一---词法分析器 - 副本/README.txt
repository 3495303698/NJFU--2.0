# 词法分析器使用指南

## 编译说明

由于Visual Studio环境变量需要正确设置，建议按照以下步骤手动编译：

1. 打开Visual Studio命令提示符（Developer Command Prompt）
   - 方法1：在开始菜单中搜索 "Developer Command Prompt"
   - 方法2：在Visual Studio中，选择 工具 > 命令行 > Developer Command Prompt

2. 在命令提示符中，导航到当前目录：
   ```
   cd "C:\Users\张政笑\OneDrive\Desktop\编译原理"
   ```

3. 运行以下编译命令：
   ```
   cl /EHsc main.cpp lexer.cpp user32.lib /Fe词法分析器.exe
   ```

4. 编译成功后，将生成 "词法分析器.exe" 文件

## 使用方法

1. 双击运行 "词法分析器.exe"
2. 在文本框中输入要分析的文件名（例如：program.txt）
3. 点击 "开始词法分析" 按钮
4. 分析结果将以表格形式显示在下方

## 注意事项

- 请确保输入的文件名正确，并且文件存在于当前目录
- 程序会显示详细的错误信息，帮助您诊断问题
- 分析结果将以表格形式展示token的类型、值、行号和列号