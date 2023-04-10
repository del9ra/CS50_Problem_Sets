#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long credit;
    credit = get_long("Number: ");
    int checksum = 0;
    int i = 0;
    int first = 0;
    int type = 0;
    int second = 0;
    while (credit != 0) // until the entered number is equal to 0
    {
        int number = credit % 10;
        i++;
        if (i % 2 == 0)
        {
            int numb = number * 2;
            while (numb != 0)
            {
                second = second + numb % 10;
                numb = numb / 10;
            }
        }
        else
        {
            first = first + number;
        }
        credit = credit / 10;
        if (credit > 9 && credit < 100)
        {
            type = credit;
        }
    }
    checksum = first + second;
    if (checksum % 10 == 0 && (i >= 13 && i <= 16)) // here is a bit tricky condition
    {
        if (type > 39 && type < 50)
        {
            printf("VISA\n");
        }
        else if (type == 34 || type == 37)
        {
            printf("AMEX\n");
        }
        else if (type > 50 && type < 56)
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
