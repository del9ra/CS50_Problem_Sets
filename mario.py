# create while loop with try except statement to catch valueerror
while True:
    try:
        height = int(input("Enter a height: "))
        if 1 <= height <= 8:
            break
    except ValueError:
        pass

# use a nested for-loop to iterate through rows and columns
for i in range(height):
    for j in range(height):
        if j < height - i - 1:
            # use end='' to combine characters in one row
            print(' ', end='')
        else:
            print('#', end='')
    print()
