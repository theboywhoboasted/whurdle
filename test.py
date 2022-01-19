import collections
import random
from wordle import Dictionary, Wordle, WORD_SIZE
from entropy import PlayWordle
import multiprocessing


def play_game(word_choice):
    game = Wordle(word_choice)
    passed, word = PlayWordle(game).play(debug=False)
    passed = passed and (word == word_choice)
    num_attempts = game.get_num_attempts()
    return (passed, word, num_attempts, word_choice)


def main():
    # play game now!
    random.seed(0)
    word_list = Dictionary().word_list
    attempts_taken = []
    uncounted_words = 0
    print(len(word_list))
    pool = multiprocessing.Pool(8)
    output = pool.map(play_game, [word.lower() for word in word_list])
    for passed, word, num_attempts, word_choice in output:
        if passed:
            attempts_taken.append(num_attempts)
        if (num_attempts > 6) or not passed:
            print("Failed on " + word_choice)
            uncounted_words += 1
    counter = collections.Counter(attempts_taken)
    print(sorted(counter.items()))
    counted_words = sum(counter.values())
    print(counted_words / (counted_words + uncounted_words))


if __name__ == "__main__":
    main()
