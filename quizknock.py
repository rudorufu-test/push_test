from itertools import permutations, product

def generate_number_permutations(numbers):
    """数の順列（並び替え）を生成する"""
    return list(permutations(numbers))

def generate_operator_combinations(length):
    """四則演算の組み合わせを生成する"""
    operators = ['+', '-', '*', '/']
    return list(product(operators, repeat=length))

def generate_expressions(numbers):
    """数の順列と演算子の組み合わせを結合して数式を作成"""
    num_permutations = generate_number_permutations(numbers)
    op_combinations = generate_operator_combinations(len(numbers) - 1)

    expressions = []

    for num_perm in num_permutations:
        for ops in op_combinations:
            expr = "".join(str(num) + op for num, op in zip(num_perm, ops)) + str(num_perm[-1])
            expressions.append(expr)

    return expressions

def insert_parentheses(expression):
    """数式に全通りの括弧を挿入する"""
    tokens = []
    num = ""

    # 数式をトークン（数字と演算子）に分割
    for char in expression:
        if char in "+-*/":
            tokens.append(num)
            tokens.append(char)
            num = ""
        else:
            num += char
    tokens.append(num)  # 最後の数値を追加

    n = (len(tokens) - 1) // 2  # 数字の数 - 1（演算子の数）

    def generate_parentheses(start, end):
        """括弧の入れ方を全通り列挙"""
        if start == end:
            return [tokens[start * 2]]  # 数字のみ

        results = []
        for mid in range(start, end):
            left_exprs = generate_parentheses(start, mid)
            right_exprs = generate_parentheses(mid + 1, end)
            op = tokens[mid * 2 + 1]

            for left in left_exprs:
                for right in right_exprs:
                    results.append(f"({left} {op} {right})")

        return results

    return generate_parentheses(0, n)

def evaluate_expression(expression):
    """数式を計算し、結果を返す（エラー時は None）"""
    try:
        result = eval(expression)
        return result
    except ZeroDivisionError:
        return None  # ゼロ除算を防ぐ
    except:
        return None  # その他の例外も無視

# 入力の受け取り
target = int(input())
nums = list(map(int, input().split()))

# ターゲットと一致する数式を探す
expressions = generate_expressions(nums)

for expr in expressions:
    for p_expr in insert_parentheses(expr):
        result = evaluate_expression(p_expr)
        if result is not None and result == target:
            print(p_expr)
            exit()  # 一致する数式が見つかったら即終了

