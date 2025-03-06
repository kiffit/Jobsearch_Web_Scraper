import string
from random import randint

# Make a function that validates strings
def input_valid_str(input_check):
    check = False
    for char in input_check:
        if char.isalpha() or char == '+':
            pass
        else:
            check = True
    if check:
        return False
    else:
        return True


# Make a function that checks if a statement executes properly, throws specified error statement otherwise
def general_check(statement, err_statement):
    bool_check = True
    try:
        check = statement()
    except:
        print(err_statement)
        bool_check = False

    if bool_check:
        return check
    else:
        return False


def check_input_valid(test_str):
    testing_chars = list(set(string.printable) - set(string.ascii_letters + "+"))
    test_str_len = len(test_str)
    pos = 0
    trues = 0
    falses = 0

    check = input_valid_str(test_str)
    print("".join(test_str), check)
    if check:
        trues += 1
    else:
        falses += 1

    for char in testing_chars:
        test_str_check = list(test_str)
        test_str_check[pos] = char
        if pos == len(test_str)-1:
            pos = 0
        else:
            pos += 1
        check = input_valid_str("".join(test_str_check))
        print("".join(test_str_check), check)

        if check:
            trues += 1
        else:
            falses += 1

    print('True: ' + str(trues) + '\nFalse: ' + str(falses))


def bad_func():
    raise Exception('This is a bad function')

def good_func():
    return True

def check_general_valid(func_range=10):
    functions = []
    good = 0
    bad = 0

    for x in range(func_range):
        num = randint(0, 1)


        if num == 1:
            functions.append(lambda: bad_func())
            bad += 1
        else:
            functions.append(lambda: good_func())
            good += 1

    for func in functions:
        check = general_check(lambda: func(), 'Error')
        if not check:
            print(func, check)
        else:
            print(func, check)

    print('Good: ' + str(good) + '\nBad: ' + str(bad))




if __name__ == '__main__':
    check_input_valid('Data+Scientist')
    print('\n\n----------------------------------------------------------\n\n')
    check_general_valid(5)

