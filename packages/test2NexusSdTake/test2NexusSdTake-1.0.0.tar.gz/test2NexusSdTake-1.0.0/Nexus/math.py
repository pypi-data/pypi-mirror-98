import random
import webbrowser as wb
# raise ValueError('A very specific bad thing happened.')

def add(a, b):

    if a != int or b != int:
        print()
        print()
        raise ValueError("Values should be int not str")
    # print("Result: ")
    elif a != str and b != str:
        return a + b

def product(a, b):
    if a != int or b != int:
        print()
        print()
        raise ValueError("Values should be int not str")
    # print("Result: ")
    elif a != str and b != str:
        return a * b

def div(a, b):
    if a != int or b != int:
        print()
        print()
        raise ValueError("Values should be int not str")
    # print("Result: ")
    elif a != str and b != str:
        return a / b

def subt(a, b):
    if a != int or b != int:
        print()
        print()
        raise ValueError("Values should be int not str")
    # print("Result: ")
    elif a != str and b != str:
        return a - b

def fraction_decimal(e, f):
    divi(e, f)

def decimal_percentage(g):
    g = float(g)
    g = g * 100
    g = g,'%'
    return g

def to_the_power(h, i):
    return h ^ i

def gen_float(j):
    p1 = random.random(0, 1)
    return j + p1

def randm(k, l):
    rand = random.ranint(k, l)
    return rand

def KO_num(m):
    m += random.random(0, 34.324238240)
    return m

def make0(n):
	n = 0
	return n

def chr_path(path):
    wb.register(
        'Chrome',
        None,
        wb.BackgroundBrowser(path)
    )

def open_calc():
    try:
        wb.get("Chrome").open('https://www.google.com/search?safe=strict&rlz=1C1CHBD_enAE775AE775&sxsrf=ALeKk03LglonBbvv6Xx5Qg1XLG66Hr70ug%3A1609823996210&ei=_PbzX6OpDIqbgQaV8JqgCQ&q=calc&oq=calc&gs_lcp=CgZwc3ktYWIQA1A0WPECYLoEaABwAXgAgAEAiAEAkgEAmAEAoAEBqgEHZ3dzLXdpesABAQ&sclient=psy-ab&ved=0ahUKEwijl8fbhYTuAhWKTcAKHRW4BpQQ4dUDCA0&uact=5')
    except Exception:
        wb.open('https://www.google.com/search?safe=strict&rlz=1C1CHBD_enAE775AE775&sxsrf=ALeKk03LglonBbvv6Xx5Qg1XLG66Hr70ug%3A1609823996210&ei=_PbzX6OpDIqbgQaV8JqgCQ&q=calc&oq=calc&gs_lcp=CgZwc3ktYWIQA1A0WPECYLoEaABwAXgAgAEAiAEAkgEAmAEAoAEBqgEHZ3dzLXdpesABAQ&sclient=psy-ab&ved=0ahUKEwijl8fbhYTuAhWKTcAKHRW4BpQQ4dUDCA0&uact=5')


def help_the_dev():
    print("Follow my GitHub: github.com/Saad-py")
    print("Thanks for using this function")

def greater_than(a, b):
    if a > b:
        return True

def less_than(a, b):
    if a < b:
        return True
        
def equal_to(a, b):
    if a == b:
        return True
    else:
        return False   


def check_the_nums(num1, num2):
    if num1 > num2:
        print(num1, 'is Greater')
    elif num2 > num1:
        print(num2, 'is Greater')
    elif num1 == num2:
        print('They are Same')

def qt():
	quit()



# 40 or 41 funcctions are done Hundreds more to go
