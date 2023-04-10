#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int x;
    do
    {
        x = get_int("Height: ");
    }
    while (x < 1 || x > 8);

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
        //Divide 2 pyramids by space
        printf("  ");

        //One more loop for another pyramid
        for (int b = 0; b <= i; b++)
        {
            printf("#");
        }
        printf("\n");

    }
