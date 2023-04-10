#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    // To prompt user for a string
    string word = get_string("Message: \n");

    //To iterate though the string
    int n = strlen(word);
    //the string
    for (int i = 0; i < n; i++)
    {
        //creating array with the size of 8 and fill with zeroes
        int j = 0;
        int array[BITS_IN_BYTE] = {0,0,0,0,0,0,0,0};

        //decimal-to-binary
        while (word[i] > 0)
        {
            int remainder = word[i] % 2;
            word[i] /= 2;
            //assign remainder to each element of the array with '[j]'
            array[j] = remainder;
            j++;
        }

        //loop to represent bits in the opposite order
        for (int l = BITS_IN_BYTE-1; l >= 0; l--)
        {
            print_bulb(array[l]);
        }
        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
