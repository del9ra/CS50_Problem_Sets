from cs50 import get_string


def main():
    # prompt to enter a text
    text = get_string("Text: ")
    # create functions to find out number of w, s and l
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)
    # formulas for calculating averages of letter and sentences
    L = letters / words * 100
    S = sentences / words * 100
    x = 0.0588 * L - 0.296 * S - 15.8
    # typecast to int
    grade = round(x)
    # find out which grade
    if grade < 1:
        print("Before Grade 1")
    elif grade >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {grade}")


def count_letters(t):
    counter = 0
    for i in t:
        # check each character
        if i.isalpha():
            counter += 1
    return counter


def count_words(t):
    counter = 0
    # check each character and + 1
    for j in t:
        if j.isspace():
            counter += 1
    return counter + 1


def count_sentences(t):
    counter = 0
    # check each character for punctuation symbol
    for x in t:
        if x in ['.', '!', '?']:
            counter += 1
    return counter


if __name__ == "__main__":
    main()
