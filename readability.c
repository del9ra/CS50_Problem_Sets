#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    //Prompt the user for a string of text
    string text = get_string("Text: ");
    float let = count_letters(text);
    float wor = count_words(text);
    float sent = count_sentences(text);

    float L = (let / wor) * 100;
    float S = (sent / wor) * 100;
    float x = (0.0588 * L) - (0.296 * S) - 15.8;

    {

        if (x >= 16)
        {
            printf("Grade 16+\n");
        }
        else if (x < 1)
        {
            printf("Before Grade 1\n");
        }
        else
        {
            int new = round(x);
            printf("Grade %i\n", new);
        }
    }
}

int count_letters(string text)

{
    //Count letters, words with space, sentences with '?.!'
    int letter = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            letter += 1;
        }
    }
    return letter;
}

int count_words(string text)
{
    int word = 0;
    for (int n = 0; n < strlen(text); n++)
    {
        if (isspace(text[n]))
        {
            word += 1;
        }
    }
    return word + 1;
}
int count_sentences(string text)
{
    int sentence = 0;
    for (int j = 0; j < strlen(text); j++)
    {

        if (text[j] == '.' || text[j] == '!' || text[j] == '?')
        {
            sentence += 1;
        }
    }
    return sentence;
}
