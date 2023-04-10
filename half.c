#include <cs50.h>
#include <stdio.h>

float half(float bill, float tax, int tip);

int main(void)
{
    float bill_amount = get_float("Bill before tax and tip: ");
    float tax_percent = get_float("Sale Tax Percent: ");
    int tip_percent = get_int("Tip percent: ");

    printf("You will owe $%.2f each!\n", half(bill_amount, tax_percent, tip_percent));
}

float half(float bill, float tax, int tip)
{
    float n;
    float tax1 = bill / 100 * tax;
    float tip1 = (bill + tax1) / 100 * tip;
    n = (bill + tax1 + tip1) / 2;

    return n;
}
