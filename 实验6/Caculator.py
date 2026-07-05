import math


def average(data):
    temp_ave = 0
    for value in data:
        temp_ave += value

    ave = temp_ave/len(data)
    return ave


def uncertainty_average(data):
    temp_un = 0
    n = len(data)
    ave = average(data)

    print(f"average: {ave}")
    
    for value in data:
        temp_un += (value-ave)**2

    unc_ave = (temp_un/(n**2-n))**0.5
    
    print(f"Uncertainty_a: {unc_ave}")
    return unc_ave


def uncertainty_b(delta):
    result = delta/(3**0.5)
    print(f"Uncertainty_b: {result}")

    return result


def uncertainty_c(data, delta):
    ua = uncertainty_average(data)
    ub = uncertainty_b(delta)

    uc = (ua**2 + ub**2)**0.5

    print(f"Uncertainty_c: {uc}")
    return uc


def regression(data_x, data_y):
    print("看好x轴和y轴!")
    temp_xy = 0
    temp_x2 = 0

    ave_x = average(data_x)
    ave_y = average(data_y)

    n = len(data_x)

    if len(data_y) != n:
        print("input error")
        return 0

    for i in range(0, n):
        temp_xy += data_x[i]*data_y[i]
        temp_x2 += data_x[i]**2

    b = (temp_xy - n*ave_x*ave_y)/(temp_x2 - n*ave_x**2)
    a = ave_y - b*ave_x

    print(f"a: {a}; b: {b}")
    return a, b


def relative(data_x, data_y):
    temp_xy = 0
    temp_x2 = 0
    temp_y2 = 0

    ave_x = average(data_x)
    ave_y = average(data_y)

    n = len(data_x)

    if len(data_y) != n:
        print("input error")
        return 0

    for i in range(0, n):
        temp_xy += data_x[i]*data_y[i]
        temp_x2 += data_x[i]**2
        temp_y2 += data_y[i]**2
        
    r = (temp_xy - n*ave_x*ave_y)/math.sqrt((temp_x2 - n*ave_x**2)*(temp_y2 - n*ave_y**2))

    print(f"relativity: {r}")
    return r


def standard_deviation(data):
    s = 0
    temp = 0
    ave = average(data)
    for value in data:
        temp += (value - ave)**2

    s = (temp/(len(data)-1))**0.5

    print(f"Sta_Deviation: {s}")
    return s


def diff(x, func):
    if x == 0:
        return (func(1e-5) - func(-1e-5)) / 2e-5
    else:
        return (func(x*(1+1e-5)) - func(x*(1-1e-5))) / (2e-5 * x)
