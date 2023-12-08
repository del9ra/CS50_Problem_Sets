from cs50 import get_float


# create while loop with try except statement to catch valueerror
def main():
    while True:
        try:
            cents = get_float("Enter sum: ")*100
            if cents > 0:
                break
        except ValueError:
            pass
    # pass cents to the get_quorters
    quoters = get_quarters(cents)
    # multiply coins number by 25, subtract quoters and store the rest of cents in cents variable
    cents -= quoters * 25
    # repeat but with other coins
    dimes = get_dimes(cents)
    cents -= dimes * 10
    nickels = get_nickels(cents)
    cents -= nickels * 5
    pennies = get_pennies(cents)
    cents -= pennies*1
    # calculate the sum
    print(int(quoters+dimes+nickels+pennies))


def get_quarters(money):
    # integer division to find out how many 25 coins we can use within this sum
    m = money//25
    return m


def get_dimes(money):
    # integer division to find out how many 10 coins we can use within this sum
    return money//10


def get_nickels(money):
    return money//5


def get_pennies(money):
    return money//1


if __name__ == "__main__":
    main()
