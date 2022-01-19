import argparse
from wordle import Wordle, Dictionary, WORD_SIZE, WordleMaxAttempts
from entropy import PlayWordle


class WordleInput:
    def __init__(self, dictionary_path):
        self.word_list = Dictionary(dictionary_path).word_list
        self._num_attempts = 0

    def get_num_attempts(self):
        return self._num_attempts

    def play(self, trial_word):
        print(trial_word)
        x = str(input("?"))
        assert len(x) == WORD_SIZE
        lm = {"w": "wrong_place", "r": "right_place", "u": "unused"}
        letter_map = [lm[y] for y in x]
        self._num_attempts += 1
        return letter_map


if __name__ == "__main__":
    instructions = """    You can use this commandline tool to solve the wordle you have on another screen.
    This tool will give you the word suggestion to be tried, and you need to feed it how right it was
    The feedback should be in the form of a five letter string like uurru
    Use the following map: u: unused, r: right_place, w: wrong_place"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--dictionary_path", required=True, help="Path to dictionary file"
    )
    args = parser.parse_args()
    mock_game = WordleInput(args.dictionary_path)
    print(instructions)
    passed, word = PlayWordle(mock_game).play(debug=True)
