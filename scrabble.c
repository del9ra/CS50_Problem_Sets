#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    //Keep track of score
    int score = 0;

    //Compute score for each character, where 'A' is 65. Z-A= 25,z-a=25(122-97),  25 is an index in [POINTS], the last element of that array
    //Score sums up scores
    for (int i = 0; i < strlen(word); i++)
    {
        if isupper(word[i])
        {
            score += POINTS[word[i] - 'A'];
        }
        else if islower(word[i])
        {
            score += POINTS[word[i] - 'a'];
        }
        //No need to add else condition for non-letter characters
    }
    return score;
}

