#include <cs50.h>
#include <ctype.h>
#include <stdio.h>


int main(void)

{
    int weeks = get_int("Number of weeks taking CS50: ");
    int hours[weeks];

    for (int i = 0; i < weeks; i++)
    {
        hours[i] = get_int("Week %i HW Hours: ", i);
    }
}
