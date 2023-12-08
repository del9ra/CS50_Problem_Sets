#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// preferences[i][j] is jth preference for voter i
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// Candidates have name, vote count, eliminated status
typedef struct
{
    string name;
    int votes;
    bool eliminated;
}
candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

// Numbers of voters and candidates
int voter_count;
int candidate_count;

// Function prototypes
bool vote(int voter, int rank, string name);
void tabulate(void);
bool print_winner(void);
int find_min(void);
bool is_tie(int min);
void eliminate(int min);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
        candidates[i].eliminated = false;
    }

    voter_count = get_int("Number of voters: ");
    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

    // Keep querying for votes
    for (int i = 0; i < voter_count; i++)
    {

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            // Record vote, unless it's invalid
            if (!vote(i, j, name))
            {
                printf("Invalid vote.\n");
                return 4;
            }
        }

        printf("\n");
    }

    // Keep holding runoffs until winner exists
    while (true)
    {
        // Calculate votes given remaining candidates
        tabulate();

        // Check if election has been won
        bool won = print_winner();
        if (won)
        {
            break;
        }

        // Eliminate last-place candidates
        int min = find_min();
        bool tie = is_tie(min);

        // If tie, everyone wins
        if (tie)
        {
            for (int i = 0; i < candidate_count; i++)
            {
                if (!candidates[i].eliminated)
                {
                    printf("%s\n", candidates[i].name);
                }
            }
            break;
        }

        // Eliminate anyone with minimum number of votes
        eliminate(min);

        // Reset vote counts back to zero
        for (int i = 0; i < candidate_count; i++)
        {
            candidates[i].votes = 0;
        }
    }
    return 0;
}

// Record preference if vote is valid
bool vote(int voter, int rank, string name)
{
    // look for a candidate called name
    for (int k = 0; k < candidate_count; k++)
    {
        if (strcmp(name, candidates[k].name) == 0)
        {
            // update preferences, where voter is voter number, rank is rank number. k is index of the name in the struct
            preferences[voter][rank] = k;
            return true;
        }
    }
    return false;
}

// Tabulate votes for non-eliminated candidates
void tabulate(void)
{
    // loop through each voter
    for (int voter = 0; voter < voter_count; voter++)
    {
        // create a rank to be able to change it only if candidates[].eliminated = true
        int rank = 0;
        // loop through indexes of name in struct
        for (int index_name = 0; index_name < candidate_count; index_name++)
        {
            // first find the index of the chosen candidate
            if (preferences[voter][rank] == index_name)
            {
                // if the candidate not eliminated, update votes by adding 1
                if (candidates[index_name].eliminated == false)
                {
                    candidates[index_name].votes += 1;
                    break;
                }
                // if candidates[].eliminated = true
                else
                {
                    // go into the next rank
                    rank += 1;
                    // set it to -1 in order not to affect the following search by changing index_name in the loop
                    index_name = -1;
                }
            }
        }
    }
}

// Print the winner of the election, if there is one
bool print_winner(void)
{
    // find a candidate who has more than half of the votes
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > voter_count / 2)
        {
            printf("%s\n", candidates[i].name);
            return true;
        }
    }
    // if nobody has majority of votes, return false
    return false;
}

// Return the minimum number of votes any remaining candidate has
int find_min(void)
{
    //assign first candidate's votes as minimum value
    int min = candidates[0].votes;
    // loop through and compare with other candidates' votes
    for (int j = 0; j < candidate_count; j++)
    {
        // a candidate must be not eliminated
        if (candidates[j].votes < min && candidates[j].eliminated == false)
        {
            min = candidates[j].votes;
        }
    }
    return min;
}

// Return true if the election is tied between all candidates, false otherwise
bool is_tie(int min)
{
    for (int x = 0; x < candidate_count; x++)
    {
        // if at least one candidate is not equal to min, then it's not a tie
        // each of them must by non-eliminated
        if (candidates[x].votes != min && candidates[x].eliminated == false)
        {
            return false;
        }
    }
    //if each candidate vote is the same, they're tied
    return true;
}

// Eliminate the candidate (or candidates) in last place
void eliminate(int min)
{
    for (int y = 0; y < candidate_count; y++)
    {
        // eliminate the candidate with fewest votes by setting it to true
        if (candidates[y].votes == min)
        {
            candidates[y].eliminated = true;
        }
    }
}
