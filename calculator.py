from texts import calc_input_description

operations = ('+', '-', '*', '/')


def calculate(expression):
    try:
        parts = list(map(lambda x: x.strip(), expression.split()))

        if len(parts) > 2 and parts[1] in operations:
            if 'j' in parts[0]:
                num1 = complex(parts[0])
            else:
                num1 = float(parts[0])

            if 'j' in parts[2]:
                num2 = complex(parts[2])
            else:
                num2 = float(parts[2])

            return f'{expression} = {perform_operation(num1, num2, parts[1])}'
        else:
            return f'Wrong format!\n{calc_input_description}'
    except ValueError:
        return f'Invalid input!\n{calc_input_description}'


def perform_operation(num1, num2, operation):
    if operation == '+':
        return num1 + num2
    elif operation == '-':
        return num1 - num2
    elif operation == '*':
        return num1 * num2
    elif operation == '/':
        if num2 == 0:
            return 'ERROR: cannot divide by zero'
        else:
            return num1 / num2
