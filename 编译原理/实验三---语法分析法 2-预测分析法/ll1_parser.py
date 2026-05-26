# LL(1) 预测分析器的核心逻辑

class LL1Parser:
    def __init__(self):
        # 定义文法规则
        self.productions = {
            'E': ['TG'],
            'G': ['+TG', '-TG', 'ε'],
            'T': ['FS'],
            'S': ['*FS', '/FS', 'ε'],
            'F': ['(E)', 'i']
        }
        
        # 定义终结符集合
        self.terminals = {'+', '-', '*', '/', '(', ')', 'i', '#'}
        
        # 定义非终结符集合
        self.non_terminals = {'E', 'G', 'T', 'S', 'F'}
        
        # 定义预测分析表 M[A, a]
        # M[A, a] 表示当非终结符A面临输入符号a时应选择的产生式
        self.parse_table = {
            # E的预测分析表项
            ('E', 'i'): 'TG',
            ('E', '('): 'TG',
            
            # G的预测分析表项
            ('G', '+'): '+TG',
            ('G', '-'): '-TG',
            ('G', ')'): 'ε',
            ('G', '#'): 'ε',
            
            # T的预测分析表项
            ('T', 'i'): 'FS',
            ('T', '('): 'FS',
            
            # S的预测分析表项
            ('S', '*'): '*FS',
            ('S', '/'): '/FS',
            ('S', '+'): 'ε',
            ('S', '-'): 'ε',
            ('S', ')'): 'ε',
            ('S', '#'): 'ε',
            
            # F的预测分析表项
            ('F', 'i'): 'i',
            ('F', '('): '(E)'
        }
    
    def validate_input(self, input_string):
        """
        验证输入字符串的合法性
        :param input_string: 输入字符串
        :return: (是否合法, 错误信息)
        """
        # 检查是否为空
        if not input_string:
            return False, "错误：输入字符串不能为空"
        
        # 检查是否以#结尾
        if not input_string.endswith('#'):
            return False, "错误：输入字符串必须以#结尾"
        
        # 检查是否包含非法字符
        allowed_chars = self.terminals
        for char in input_string:
            if char not in allowed_chars:
                return False, f"错误：包含非法字符 '{char}'，允许的字符为：+ - * / ( ) i #"
        
        # 检查括号是否匹配
        bracket_count = 0
        for char in input_string:
            if char == '(':
                bracket_count += 1
            elif char == ')':
                bracket_count -= 1
                if bracket_count < 0:
                    return False, "错误：括号不匹配，右括号过多"
        
        if bracket_count > 0:
            return False, "错误：括号不匹配，左括号过多"
        
        return True, ""
    
    def parse(self, input_string):
        """
        执行LL(1)预测分析
        :param input_string: 输入字符串，以#结束
        :return: 分析过程的步骤列表和分析结果，错误信息
        """
        # 验证输入
        is_valid, error_msg = self.validate_input(input_string)
        if not is_valid:
            steps = [{
                'step': 1,
                'stack': '#E',
                'input': input_string,
                'production': f'分析出错: {error_msg}'
            }]
            return steps, False, error_msg
        
        # 初始化分析栈，#是栈底符号，E是开始符号
        stack = ['#', 'E']
        
        # 初始化输入指针
        input_index = 0
        
        # 存储分析过程的步骤
        steps = []
        
        # 当前步骤号
        step_count = 1
        
        try:
            # 分析循环
            while stack[-1] != '#':
                # 确保输入指针没有越界
                if input_index >= len(input_string):
                    raise SyntaxError("语法错误：输入字符串过早结束")
                
                # 获取栈顶符号
                top = stack[-1]
                
                # 获取当前输入符号
                current_input = input_string[input_index]
                
                # 记录当前状态
                steps.append({
                    'step': step_count,
                    'stack': ''.join(stack),
                    'input': input_string[input_index:],
                    'production': ''
                })
                step_count += 1
                
                # 情况1：栈顶是终结符
                if top in self.terminals:
                    if top == current_input:
                        # 终结符匹配，弹出栈顶并移动输入指针
                        stack.pop()
                        input_index += 1
                        steps[-1]['production'] = f'匹配 {top}'
                    else:
                        # 终结符不匹配，报错
                        expected = top
                        actual = current_input
                        raise SyntaxError(f"语法错误：在位置 {input_index} 处期望 '{expected}'，但遇到 '{actual}'")
                
                # 情况2：栈顶是非终结符
                elif top in self.non_terminals:
                    # 查找预测分析表
                    if (top, current_input) in self.parse_table:
                        production = self.parse_table[(top, current_input)]
                        steps[-1]['production'] = f'{top}->{production}'
                        
                        # 弹出栈顶非终结符
                        stack.pop()
                        
                        # 将产生式右部反向压入栈中（跳过ε）
                        if production != 'ε':
                            for symbol in reversed(production):
                                stack.append(symbol)
                    else:
                        # 分析表中没有对应的产生式，报错
                        raise SyntaxError(f"语法错误：无法处理非终结符 '{top}' 面临输入符号 '{current_input}'")
                
                else:
                    # 非法符号
                    raise SyntaxError(f"语法错误：栈中存在非法符号 '{top}'")
            
            # 检查输入是否已全部处理
            if input_index == len(input_string) - 1 and input_string[input_index] == '#':
                # 分析成功
                steps.append({
                    'step': step_count,
                    'stack': ''.join(stack),
                    'input': input_string[input_index:],
                    'production': '分析成功'
                })
                return steps, True, ""
            else:
                raise SyntaxError(f"语法错误：输入字符串未完全处理，剩余部分: {input_string[input_index:]}")
        
        except SyntaxError as e:
            # 记录错误信息
            steps.append({
                'step': step_count,
                'stack': ''.join(stack),
                'input': input_string[input_index:] if input_index < len(input_string) else '',
                'production': f'分析出错: {str(e)}'
            })
            return steps, False, str(e)