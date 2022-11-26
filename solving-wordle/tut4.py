m = lambda x : x * 2
square = lambda x : x*x

def gradient_descent_tabulation(x_i, iter, alpha, gradient):
    print(f"Alpha: {alpha}")
    print(f"({x_i}, {square(x_i)})")
    curr_x = x_i
    for i in range(iter):
        curr_x = curr_x - alpha * gradient(curr_x)
        print(f"({curr_x}, {square(curr_x)})")

gradient_descent_tabulation(5, 5, 10, m)
gradient_descent_tabulation(5, 5, 1, m)
gradient_descent_tabulation(5, 5, 0.1, m)
gradient_descent_tabulation(5, 5, 0.01, m)