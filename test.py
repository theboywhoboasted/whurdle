import argparse
import collections
import random
from wordle import Dictionary, Wordle, WORD_SIZE
from entropy import PlayWordle
import multiprocessing


def play_game(args):
    word_choice, dictionary_path, target_dictionary_path = args[:3]
    game = Wordle(word_choice, dictionary_path)
    passed, word, styles = PlayWordle(
        game, target_dictionary_path=target_dictionary_path
    ).play(debug=False)
    passed = passed and (word == word_choice)
    num_attempts = game.get_num_attempts()
    return (passed, word, num_attempts, word_choice, styles)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--dictionary_path",
        required=True,
        help="Path to dictionary file for valid words",
    )
    parser.add_argument(
        "--target_dictionary_path",
        required=False,
        default=None,
        help="Path to dictionary file for the target words if not the same as valid words",
    )
    parser.add_argument(
        "-n",
        "--num_samples",
        required=False,
        default=None,
        type=int,
        help="Number of sampled words to use to test",
    )
    args = parser.parse_args()
    if args.target_dictionary_path is None:
        args.target_dictionary_path = args.dictionary_path

    word_list = Dictionary(args.target_dictionary_path).word_list
    print(len(word_list))
    pool = multiprocessing.Pool(8)
    if args.num_samples:
        random.seed(0)
        lower_word_list = [
            (word.lower(), args.dictionary_path, args.target_dictionary_path)
            for word in random.sample(word_list, args.num_samples)
        ]
    else:
        lower_word_list = [
            (word.lower(), args.dictionary_path, args.target_dictionary_path)
            for word in word_list
        ]
    output = pool.map(play_game, lower_word_list)
    attempts_taken = []
    failed_words = []
    for passed, word, num_attempts, word_choice, styles in output:
        if passed:
            attempts_taken.append(num_attempts)
        if (num_attempts > 6) or not passed:
            failed_words.append(word_choice)
        if "overlap" in styles:
            print(word_choice)
    print("Failed on {}".format(sorted(failed_words)))
    counter = collections.Counter(attempts_taken)
    print(sorted(counter.items()))
    counted_words = sum(counter.values())
    print(counted_words / (counted_words + len(failed_words)))


if __name__ == "__main__":
    main()
