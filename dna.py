import csv
import sys


def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Error! Enter 2 file names")
    if not sys.argv[1].endswith(".csv") or not sys.argv[2].endswith(".txt"):
        sys.exit("Error! Enter csv and text file name")
    str_matches = dict()
    try:
        # Read database file into a variable
        with open(sys.argv[1]) as file:
            d_reader = csv.DictReader(file)
            headers = d_reader.fieldnames[1:]
            list_of_data = list(d_reader)
    except FileNotFoundError:
        print("File not found")

    # Read DNA sequence file into a variable
    f = open(sys.argv[2])
    txt_file = f.read()

    # Find longest match of each STR in DNA sequence
    for i in headers:
        str_matches[i] = longest_match(txt_file, i)

    # Check database for matching profiles
    # i - index of each line/dict in list_of_data
    check = False
    for i in range(len(list_of_data)):
        # str - each str
        for str in str_matches:
            # checking every str on each line
            if (
                int(list_of_data[i][str]) == str_matches[str]
            ):  # compare two same str-names
                check = True
                # assign name by addressing through indexes
                name = list_of_data[i]["name"]
            else:
                # even if one of strs in the line is wrong stop
                check = False
                break
        # if each of the strs is True break and print
        if check:
            break

    if check:
        print(name)
    else:
        # else if no match, print this
        print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
