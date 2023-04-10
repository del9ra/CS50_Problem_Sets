#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //Prompt a user to input height with do... while... loop
    int x;
    do
    {
        x = get_int("Height: ");
    }
    //Use operators to set the range
    while (x < 1 || x > 8);

    //Create nested loops and conditional statements to make dots and hashes
    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < x; j++)
        {
            if (j < x - i - 1)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        printf("\n");
    }
}

