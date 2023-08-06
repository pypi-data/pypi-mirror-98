  
def NOT(a):
    if a == 0:
        return(1)
    elif a == 1:
        return(0)
    else:
        print("This type is not in the database")


def AND(a, b):
    if a == 1 and b == 1:
        return(1)
    else:
        return(0)


def OR(a, b):
    if a == 0 and b == 0:
        return(0)
    else:
        return(1)


# Nor gate is when we first use an or gate then use that output for a NOT gate
def NOR(a, b):
    if a == 0 and b == 0:

        return(1)
    else:
        return(0)


def NAND(a, b):
    if a == 1 and b == 1:
        return(0)
    else:
        return(1)


# AND   |   OR   |   NOT  |   NOR

# To convert bin to int
def bint(n):
    return int(n)


#  To convert int to bin

def dbin(n):
    return bin(n)

def XNOR(a, b):
    if a == 0 and b == 0 or a == 1 and b == 1:
        return 1

def XOR(a, b):
    if a == 1 and b == 1:
        return 0
    elif a == 0 and b == 0:
        return 0
    else:
        return 1


