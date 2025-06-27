polynomial = input('Input the polynomials : ')
def split(polynomial):
    polynomial = polynomial.replace('(', '')
    polynomial = polynomial.replace('-', '%-') #為了之後能讓負號保留
    polynomial = polynomial.replace('+', '%') 
    polynomial_split = polynomial.split(')')
    del polynomial_split[-1]

    split_by_add_minus = []
    for i in polynomial_split: #去除空項
        no_space = []
        inside_split = i.split('%')
        for j in inside_split:
            if j:
                no_space.append(j)
        split_by_add_minus.append(no_space)
    return split_by_add_minus

def term(polynomial):
    coeff = ''
    var = ''
    found_coeff = False

    for char in polynomial:
        if char.isdigit() or char == '-' or char == '+':
            if not found_coeff:
                coeff += char  # 如果還沒找到變數，則字符視為係數的一部分
            else:
                var += char  # 如果已經找到變數，則字符視為變數的一部分
        else:
            found_coeff = True
            var += char  # 找到第一個字母後，視為變數的開始

    # 處理係數為空或只有正負號的情況
    if coeff == '' or coeff == '+':
        coeff = 1
    elif coeff == '-':
        coeff = -1
    else:
        coeff = int(coeff)
    return coeff, var


def multiply_terms(term1, term2):
    coeff1, var1 = term(term1)
    coeff2, var2 = term(term2)
    
    # 係數相乘
    coeff_result = coeff1 * coeff2
    
    # 變數相乘 假設變數不同時合併變數
    if var1 == '' and var2 == '':
        return str(coeff_result)
    elif var1 == '':
        return f'{coeff_result}{var2}'
    elif var2 == '':
        return f'{coeff_result}{var1}'
    else:
        return f'{coeff_result}{var1}{var2}'


def multiply_polynomials(polynomial):
    split_polynomials = split(polynomial)
    first_terms = split_polynomials[0]  # 從第一個多項式開始

    # 從第二個多項式開始逐一與結果相乘
    for i in range(1, len(split_polynomials)):
        current_terms = split_polynomials[i]
        new_result = []
        # 與當前多項式的每一項進行相乘
        for term1 in first_terms:
            for term2 in current_terms:
                new_result.append(multiply_terms(term1, term2))
        # 更新 first_terms 為新的乘積結果
        first_terms = new_result
    return first_terms


def merge_expo(variables):
    merged = {}
    for var, coeff in variables.items():
        # 統計字母出現次數
        letter_count = {}
        i = 0
        while i < len(var):
            letter = var[i]  # 當前的字母
            i += 1
            exponent = 1  # 默認次方為1
            
            # 檢查是否有次方標記 '^'
            if i < len(var) and var[i] == '^':
                i += 1  # 跳過 '^'
                exp_str = ''
                
                # 處理數字次方
                while i < len(var) and var[i].isdigit():
                    exp_str += var[i]
                    i += 1
                exponent = int(exp_str) if exp_str else 1

            # 合併相同的字母
            if letter in letter_count:
                letter_count[letter] += exponent  # 字母已經出現過，增加次方
            else:
                letter_count[letter] = exponent  # 新的字母，記錄次方

        # 構造合併後的變數字串
        merged_var = ''
        for letter, count in sorted(letter_count.items()):  # 按字母排序
            if count == 1:
                merged_var += letter
            else:
                merged_var += f'{letter}^{count}'

        # 合併相同變數的係數
        if merged_var in merged:
            merged[merged_var] += coeff
        else:
            merged[merged_var] = coeff

    return merged


def merge_term(polynomial):
    raw_result = multiply_polynomials(polynomial)
    variables = {}
    for i in raw_result:
        # 去掉 '*'
        i = i.replace('*', '')
        
        # 分離係數和變數
        coeff = ''
        var = ''
        found_coeff = False

        for char in i:
            if char.isdigit() or char == '-' or char == '+':
                if not found_coeff:
                    coeff += char  # 係數的一部分
                else:
                    var += char  # 變數的一部分
            else:
                found_coeff = True
                var += char  # 第一個字母後面的字符都視為變數
        # 處理係數為空或只有正負號的情況
        if coeff == '' or coeff == '+':
            coeff = 1
        elif coeff == '-':
            coeff = -1
        else:
            coeff = int(coeff)
        
        # 合併相同的變數項
        if var in variables:
            variables[var] += coeff
        else:
            variables[var] = coeff
    return merge_expo(variables)


def print_out(polynomial):
    polynomial_str = ''
    result = merge_term(polynomial)
    for key in result:
        coeff = result[key]
        if coeff == 1:
            if polynomial_str == '':
                polynomial_str += f'{key}'
            else:
                polynomial_str += f'+{key}'
        elif coeff == -1:
            if polynomial_str == '':
                polynomial_str += f'-{key}'
            else:
                polynomial_str += f'-{key}'
        else:
            if polynomial_str == '':
                polynomial_str += f'{coeff}*{key}'
            elif coeff > 0:
                polynomial_str += f'+{coeff}*{key}'
            else:
                polynomial_str += f'{coeff}*{key}'
    return polynomial_str
        

# 測試
print(print_out(polynomial))
