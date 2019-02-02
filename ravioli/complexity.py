import re


# Calculate the complexity of all the the functions in a string.
def calculate_complexity(code):
    results = {}
    function_matcher = re.compile(r'\s+(\w+)\s*\(.*\)\s*{', re.MULTILINE)

    for m in function_matcher.finditer(code):
        name = m.group(1)
        if __is_a_function(name):
            start_of_function = m.end()
            # We just found the next function. Extract the body of the function.
            function_body = __extract_next_function_body(code[start_of_function:])
            # Compute the complexity of this function.
            results[name] = __calculate_complexity_for_a_function(function_body)

    return results


# Determine if this name is keyword that makes a decision/
def __is_a_decision(name):
    decision_keywords = ['if', 'while', 'for']
    return name in decision_keywords


# Determine if this name is a function (and not a keyword that looks like one).
def __is_a_function(name):
    keywords_that_look_like_functions = ['if', 'while', 'for', 'switch']
    return name not in keywords_that_look_like_functions


# Extract the next function body in this section of code by matching braces.
def __extract_next_function_body(code):
    i = 0
    brace_nesting = 1
    while brace_nesting > 0:
        if code[i] == '{':
            brace_nesting += 1
        elif code[i] == '}':
            brace_nesting -= 1
        i += 1
    end_index = i
    return code[:end_index]


# Calculate the complexity of a function.
def __calculate_complexity_for_a_function(body):
    complexity = 1

    # Find if, while and for statements.
    keyword_matcher = re.compile(r'[\s}]+(\w+)\s*\(.*\)', re.MULTILINE)
    for m in keyword_matcher.finditer(body):
        name = m.group(1)
        if __is_a_decision(name):
            complexity += 1

    # Find case statements.
    case_matcher = re.compile(r'\s+case\s+')
    complexity += len(case_matcher.findall(body))
    return complexity
