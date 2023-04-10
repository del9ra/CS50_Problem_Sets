#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int x;
    do
    {
        x = get_int("Starting size: ");
    }
    while (x<9);

    int y;
    do
    {
        y = get_int("Ending size: ");
    }
    while (y<x);

    int n=0;
    while (x<y)
    {
        x=x+x/3-x/4;
        n++;
    }
    printf("Years: %i\n", n);
}
