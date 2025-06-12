#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_mul(line, index):
    token = {'type': 'MUL'}
    return token, index + 1

def read_div(line, index):
    token = {'type': 'DIV'}
    return token, index + 1

def read_par_open(line, index):
    token = {'type': 'PAR_OPEN'}
    return token, index + 1

def read_par_close(line, index):
    token = {'type': 'PAR_CLOSE'}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_mul(line, index)
        elif line[index] == '/':
            (token, index) = read_div(line, index)
        elif line[index] == '(':
            (token, index) = read_par_open(line, index)
        elif line[index] == ')':
            (token, index) = read_par_close(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    #tokens.insert(0, {'type': None})
    print(tokens)
    return tokens

def compute_parentheses(tokens):
    i = 0
    while i < len(tokens):
        if tokens[i]['type'] == 'PAR_OPEN':
            depth = 1
            j = i + 1
            while j < len(tokens) and depth:
                if tokens[j]['type']=='PAR_OPEN':
                    depth += 1
                elif tokens[j]['type']=='PAR_CLOSE':
                    depth -= 1
                j += 1
            if depth != 0:
                raise SyntaxError("Unmatched '('")
            in_par = tokens[i+1:j-1]
            in_par = compute_parentheses(in_par)
            compute = evaluate(in_par, compute_mul_and_div(in_par))
            tokens[i:j] = [{'type':'NUMBER', 'number': compute}]
        else:
            i += 1
    return tokens

"""
+-1.0+2.1-3*4/5
+-3*4*5
+3/4
test("(3.0 + 4 * (2 − 1)) / 5")
test("((3*4)+(4/5)) - 6")
+-3*4+5/6
"""

# +-3*4+1+2+5/6


# # +[-3*4]+1+2[+5/6]

# +[-3*4]+1+2[+5/6*7]
# (-3*4+5/6*7)+1+2
# (-3*4+5/6)*7+1+2

# +[-3*4]+1+2[+5/6*7]
#   -12       

# +[-3*4]+1+2[+5/6]*7
# +[nnnn]+1+2nn[nn*7]

# +[-3*4]+1+2+[5/6*7]



# +, -, 3, *, 4, *, 5   0
# +, None, None, None, None, *, 5   -12
# +, None, None, None, None, None, None   -60

def compute_mul_and_div(tokens):
    prod = 0
    count = 0 
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index2 = 1
    #can be fixed to index
    #replace the None to whatever intermediate value and replace, but be careful of index tracking
    while index2 < len(tokens):
        if tokens[index2]['type'] == 'NUMBER':
            if tokens[index2 - 1]['type'] == 'MUL':
                if tokens[index2 - 3]['type'] == 'PLUS':
                    count +=  tokens[index2 - 2]['number'] * tokens[index2]['number']
                    tokens[index2 - 3]['type'] = None
                    tokens[index2 - 2]['type'] = None
                    tokens[index2 - 1]['type'] = None
                    tokens[index2]['type'] = None
                elif tokens[index2 - 3]['type'] == 'MINUS':
                    count -= tokens[index2 - 2]['number'] * tokens[index2]['number']
                    tokens[index2 - 3]['type'] = None
                    tokens[index2 - 2]['type'] = None
                    tokens[index2 - 1]['type'] = None
                    tokens[index2]['type'] = None
                else:
                    count *= tokens[index2]['number']
                    tokens[index2 - 1]['type'] = None
                    tokens[index2]['type'] = None
                if index2 == len(tokens)-1 or \
                    tokens[index2 + 1]['type'] != 'MUL' and tokens[index2 + 1]['type'] != 'DIV':
                    prod += count
                    count = 0
            elif tokens[index2 - 1]['type'] == 'DIV':
                if tokens[index2 - 3]['type'] == 'PLUS':
                    count +=  tokens[index2 - 2]['number'] / tokens[index2]['number']
                    tokens[index2 - 3]['type'] = None
                    tokens[index2 - 2]['type'] = None
                    tokens[index2 - 1]['type'] = None
                    tokens[index2]['type'] = None
                elif tokens[index2 - 3]['type'] == 'MINUS':
                    count -= tokens[index2 - 2]['number'] / tokens[index2]['number']
                    tokens[index2 - 3]['type'] = None
                    tokens[index2 - 2]['type'] = None
                    tokens[index2 - 1]['type'] = None
                    tokens[index2]['type'] = None
                else:
                    count /= tokens[index2]['number']
                    tokens[index2 - 1]['type'] = None
                    tokens[index2]['type'] = None
                if index2 == len(tokens)-1 or \
                    tokens[index2 + 1]['type'] != 'MUL' and tokens[index2 + 1]['type'] != 'DIV':
                    prod += count
                    count = 0
        index2 += 1
    return prod

def evaluate(tokens, answer):
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == None:
            index += 1
            continue
        elif tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == None:
                index += 1
                continue
            elif tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                #print(tokens[index])
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

def test(line):
    tokens = tokenize(line)
    tokens = compute_parentheses(tokens)
    actual_answer = evaluate(tokens, compute_mul_and_div(tokens))
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))

# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("1.0+2.1-3*4")
    test("1.0+2.1-3*4/5")
    #test("1.0+2.1-3a4/5")
    #test("")
    test("1")
    test("-1*9+2.0")
    test("(3.0+4*(2-1))/5")
    test("((3*4)+(4+5))-6")
    test("-3*4+5/6")
    test("-3*4+5*6/7")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    tokens = compute_parentheses(tokens)
    answer = evaluate(tokens, compute_mul_and_div(tokens))
    print("answer = %f\n" % answer)