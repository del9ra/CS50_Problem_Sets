#include <cs50.h>
#include <stdio.h>
#include <string.h>
// Declare function to replace letters with digits
string replace(string new);
//argc is responsible for counter, argv for string
int main(int argc, string argv[])

{
//Print error(return 1) if a string is empty or has more than one command-line argument
    if (argc == 1 || argc > 2)
    {
        printf("Usage: ./no-vowels word\n");
        return 1;
    }
//Call replace function for other cases, implying one argument
    else
    {
        printf("%s\n", replace(argv[1]));
        return 0;
    }
}


string replace(string new)
{
    //Iterate elements of the string
    for (int i = 0; i < strlen(new); i++)
    {
        //If a character equals a vowel, replace it, using switch statement
        switch (new[i])
        {
            // case means 'if smth equals...'
            case 'a':
                new[i] = '6';
                break;
            case 'e':
                new[i] = '3';
                break;
            case 'i':
                new[i] = '1';
                break;
            case 'o':
                new[i] = '0';
                break;
        }
    }
    return new;
}
