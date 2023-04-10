#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int length;
    do
    {
        length = get_int("Length: ");
    }
    while (length < 1);

    //Declare array
    int twice [length];
    //Set the first value
    twice[0] = 1;
    printf("%i\n", twice[0]);
    for(int i = 1; i < length; i++)
    {
        //Make the current element twice the previous

        twice[i] = 2 * twice[i - 1];

        //Print the current element
        printf("%i\n", twice[i]);
    }
}
