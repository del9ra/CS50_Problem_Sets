#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

bool valid(string password);

int main(void)
{
    string password = get_string("Enter your password: ");
    if (valid(password))
    {
        printf("Your password is valid!\n");
    }
    else
    {
        printf("Your password needs at least one uppercase letter, lowercase letter, number and symbol\n");
    }
}

bool valid(string password)
{
    //Create 4 boolean variables for each element(upper/lower, digits, symbol)
    bool lower = false;
    bool upper = false;
    bool digit = false;
    bool symbol = false;

    //Iterate through the string
    for (int i = 0; i < strlen(password); i++)
    {
        //Use fuctions from ctype library, change boolean expression to true
        if (islower(password[i]))
        {
            lower = true;
        }
        else if (isupper(password[i]))
        {
            upper = true;
        }
        else if (isdigit(password[i]))
        {
            digit = true;
        }
        else if (ispunct(password[i]))
        {
            symbol = true;
        }
    }
    //return boolean variable results
    return lower && upper && digit && symbol;
}
