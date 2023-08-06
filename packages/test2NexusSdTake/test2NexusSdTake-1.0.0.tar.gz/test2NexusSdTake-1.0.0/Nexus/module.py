import importlib


def HELP():
    print(
        "Your Guide to this part of NEXUS\n",
        "This part of NEXUS will help you import modules in python very easily\n",
        "For example I want to import numpy and pandas\n",
        "The Code: \n",
        "# First import the module part of the nexus module refer to the docs or the github repo for NEXUS\n"
        "np = module.np()\n"
        "#Test it\n"
        "print(np.array([1,2,3,4])\n"

        "For any more help create a stack overflow and send the link in a github issue on the NEXUS repo, OR you can "
        "directly open an issue on the NEXUS repo\n "
        "Hope this helps  :)"
    )


def ipm(md):
    return importlib.import_module(md)


def np():
    return ipm("numpy")


def pd():
    return ipm("pandas")


def sklearn():
    return ipm("sklearn")


def lin_model():
    return ipm("sklearn.linear_model")


def linear_regression():
    return ipm("sklearn.linear_model.LinearRegression")


def torch():
    return ipm("torch")


def tensorflow():
    return ipm("tensorflow")


def pyplot():
    return ipm("matplotlib.pyplot")


def scipy():
    return ipm("scipy")


def selenium():
    return ipm("selenium")


def opencv():
    return ipm("cv2")


def bs4():
    return ipm("bs4")


def module(md):
    return ipm(md)


def random():
    return ipm("random")


def math():
    return ipm("math")


def os():
    return ipm("os")


def sys():
    return ipm("sys")


def socket():
    return ipm("sockets")


def pickle():
    return ipm(
        "pickle"
    )


def time():
    return ipm("time")


def dtime():
    return ipm("datetime")


def cgi():
    return ipm("cgi")


def re():
    return ipm("re")


def ulib():
    return ipm("urllib")


def ulib3():
    return ipm("urllib3")

