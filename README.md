# whurdle
# A Solver for Wordle

I looked at Wordle as a more complex version of the counterfeit coin puzzle (https://en.wikipedia.org/wiki/Balance_puzzle). In both games, we can ask a specific kind of questions to an answering machine to extract information. After asking a few questions, we have enough information to uncover the solution. In the counterfeit coin puzzle, the weighing scale is the answering machine that tells you whether the two sides are balanced, and if not, which side is heavier. In Wordle, the answering machine tells us which letters of our query word exist in the target word (and among the ones that do, whether they are at the right place). We start with a long list of words (all the 5-letter dictionary words) and make a few invocations to the answering machine. Each invocation gives us partial information that helps to reduce the set of words until there is exactly one word left. The initial list is thousands of words long and we get six tries. On average we need to eliminate 75% to 80% of the words with each try.

# My Algorithm

My solver for Wordle is a greedy algorithm i.e. I try to maximize the information I can get from the answering machine in each invocation. In my implementation, I assign each 5-letter word in the dictionary a score to quantify how much information it can extract and pick the word with the highest score. To understand how this score is computed, we need to remember the two kinds of information we get from each invocation:
1. whether each letter in the attempted word exists in the target word or not
2. for the letter in the attempted word that exists in the target word, whether it is at the right place

The scoring mechanism should thus combine both these kinds of information. My definition of a word score is the sum of the unordered (1) and ordered word score (2).

To define the unordered score, the main observation is that we do not want to try letters that are either too likely or too unlikely. If we choose a letter that is very unlikely (say 'q'), it will give us a lot of information if it exists in the target word, but the likelihood of it existing in the target word is low. Hence on average, we get very little information from such letters. Similarly, if a letter is very likely to exist (say 'u' if you already know that the word has 'q' in it), it doesn't give a lot of information since it eliminates very few words. It may still be valuable from a positioning point of view, but we are talking about the unordered score here. Hence I have defined the unordered score as sum_i(p_i\*(1-p_i)) where p_i is the probability that the i^th letter of the word would exist in the target word. There is nothing unique about this scoring function: I just chose something that reflects the idea of the score being low if the probability is too low or too high. 

The ordered score is defined similarly, except that the probability is defined for each position in the word. The total score is simply the sum of the ordered and unordered scores.

# Accuracy numbers

The success rate of the above algorithm is heavily dependent on which dictionary I use as the universe of all words. A larger dictionary will make for a bigger universe to search for, but will also allow me to choose from more words on each try. Having said that, the algorithm gets 99%+ words solved within 6 attempts with all the dictionaries I tried. Most of the words that it is unable to solve are the ones with repeated letters or words with too many adjacent words (i.e. words that differ from the target word by only 1 letter). I report here the results for 3 common English dictionaries:

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

My current implementation can be greatly improved with the use of better data for computing the probabilities and hence the word scores. I worked under the assumption that the target word to be discovered is chosen uniformly at random from the dictionary of all 5-letter words and the same dictionary is used to validate the attempted word-tries. I discovered this blog post (https://lockwood.dev/wordle/python/2022/01/23/wordle-solved-average-3-64.html) that mentions that this is indeed not true. While there are around 10k words that can be tried, only a quarter of those could be the target word. I'll update this post soon with the accuracy of my solver using this information. 

Secondly, the algorithm that I have implemented is greedy. Thinking about more than one step at a time is computationally expensive in general, but it might be a good idea to do when we have very few words left to search from. The current solver does a bad job with words with too many adjacent words where it filters down to a fairly small number of words in the first couple of tries but struggles to move forward from there. This might be a good place to try a multi-step strategy.

Finally, the scoring functions that I have chosen are the first things that came to my mind. There is no argument against against using (-p_i\*log(p_i)) instead of (p_i\*(1-p_i)), except maybe it might take a little longer to compute. There is no dearth of interesting scoring mechanisms that could be tried to get to a better accuracy level.

# Acknowledgements

Sincere Thanks to Gary and Charu for introducing me to the game and helping me work through the various iterations of the algorithm. You are both awesome!
