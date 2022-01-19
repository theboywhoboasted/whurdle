# whurdle
# A Solver for Wordle

I looked at Wordle as a more complex version of the counterfeit coin puzzle (https://en.wikipedia.org/wiki/Balance_puzzle). You start with a long list of words (all the 5-letter dictionary words) and make a few invocations to an oracle. Each invocation gives you partial information that helps you reduce your set of words until you are left with exactly one. In this case, the initial list is thousands of words and you get six tries. On average you would need to eliminate 75% to 80% of the words with each try.

# Current Algorithm

What I have implemented here is a greedy algorithm where at every attempt, I try to maximize the information I can get from the oracle. A better (and significantly more complex) solution would be to consider two or three steps at a time. In my implementation, I score each 5-letter word in the dictionary based on how much information it can extract and use the highest score. One important assumption in my solution is that each word in the dictionary is equally likely to be the target word.

Now, each word tried with the oracle gives us two kinds of information:
1. whether each letter in the attempted word exists in the target word or not
2. for the letter in the attempted word that exists in the target word, whether it is at the right place
The scoring mechanism should thus combine both these kinds of information. My definition of a word score is the sum of the unordered (1) and ordered word score (2).

To define the unordered score, the main observation is that we do not want to try letters that are either too likely or too unlikely. If we choose a letter that is very unlikely (say 'q'), it will give us a lot of information if it exists in the target word, but the likelihood of it existing in the target word is low. Hence on average, we get very little information from such letters. Similarly, if a letter is very likely to exist (say 'u' if you already know that the word has q in it), it doesn't give a lot of information since it eliminates very few words. It may still be valuable from a positioning point of view, but we are talking about the unordered score here. Hence I have defined the unordered score as sum_i(p_i\*(1-p_i)) where p_i is the probability that the i^th letter of the word would exist in the target word.

I define the ordered score in a similar way except that the probability is defined for each position in the word. The total score is simply the sum of the ordered and unordered scores. This simple algo is good enough for most words and I was able to get 99.2% cases solved within 6 attempts by this simple scoring method. Most of the words that it is unable to solve are the ones with repeated letters or words with too many adjacent words (i.e. words that differ from the target word by only 1 letter).

# Accuracy numbers

How well the current solver depends on which dictionary I use as the universe of all words. A dictionary with a larger set of words makes for a bigger set of words to search from but also makes it easier to search given the larger set to choose from for each try. I report here the results for 3 common English dictionaries:

1. dictionary.csv (a valid scrabble dictionary from https://github.com/zeisler/scrabble)
Number of words: 8636
Accuracy: 99.45%
Failed words: ['cacas', 'dared', 'dived', 'dodos', 'dowed', 'eaves', 'faked', 'fifes', 'fixed', 'gests', 'gives', 'hives', 'hover', 'jades', 'jakes', 'jeers', 'jills', 'jiver', 'jives', 'rater', 'reefs', 'rider', 'riper', 'sakes', 'saves', 'seers', 'setts', 'sills', 'sines', 'sinks', 'sises', 'sixes', 'sizes', 'sooks', 'stets', 'tates', 'tests', 'tight', 'vests', 'wakes', 'waves', 'wests', 'wises', 'wooed', 'wowed', 'zests', 'zills']
Attempt counter: [(1, 1), (2, 43), (3, 1612), (4, 4556), (5, 2040), (6, 337)]

2. unix_words.txt (Standard Unix dictionary from https://raw.githubusercontent.com/dolph/dictionary/master/unix-words)
Number of words: 9972
Accuracy: 99.81%
Failed words: ['cinch', 'eager', 'faffy', 'folly', 'gager', 'hexer', 'jinny', 'lolly', 'mimer', 'oolly', 'pappy', 'poppy', 'rager', 'raver', 'rever', 'roker', 'rover', 'yappy']
Attempt counter: [(1, 1), (2, 34), (3, 1688), (4, 5373), (5, 2588), (6, 270)]

3. sgb-words.txt (Knuth's Stanford Graph Base at https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt)
Number of words: 5757
Accuracy: 99.89%
Failed words: ['faxed', 'folly', 'jells', 'loses', 'loves', 'soles']
Attempt counter: [(1, 1), (2, 42), (3, 1417), (4, 3087), (5, 1038), (6, 166)]

# Suggested Improvements

There are a few ways the current algo can be made better. I alluded to the fact earlier that one mgiht be able to do better by thinking of more than 1 step at a time. This may be intractable for all cases but in the harder cases (where the current solver either fails or takes too many attempts), the solver often gets to a very small subset of words in the first 2-3 tries but struggles to get to the right word in the remaining attempts. Further, the scoring function could be parametrized and one could train the parameters to get a better success rate.
