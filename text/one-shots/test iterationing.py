tokens = "this is a decent enough test sentence".split(" ")
cap = len(tokens)
degree = 2


for ti in range(cap):
    lower = ti if ti < degree else degree
    upper = cap - ti -1 if ti >= cap - degree -1 else degree
    # the -1 is because (range(1, 1) won't run once for 1
    for i in range(upper):
        print(i, ti, ti + i +1, upper, cap, degree)
        print(tokens[ti], tokens[ti+i+1])
