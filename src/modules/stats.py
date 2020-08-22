from scipy.stats import shapiro

def shapiro_wilk_test(data):
    # normality test
    stat, p = shapiro(data)
    print('Statistics=',stat,'p=',p)
    # interpret
    if (p > 0.05):
        print('Sample looks Gaussian')
    else:
        print("Sample doesn't look Gaussian")