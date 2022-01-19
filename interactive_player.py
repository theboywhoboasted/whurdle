from wordle import Wordle, Dictionary, WORD_SIZE, WordleMaxAttempts
from entropy import PlayWordle


class WordleInput:
    def __init__(self):
        self.word_list = Dictionary().word_list
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
    mock_game = WordleInput()
    passed, word = PlayWordle(mock_game).play(debug=True)
