import argparse
import getpass
from colorama import Fore, Back, Style

WORD_SIZE = 5
NUM_ATTEMPTS = 6


class Dictionary:
    def __init__(self, text_path):
        word_list = []
        with open(text_path) as f:
            for line in f:
                word = line.strip().lower()
                if len(word) == WORD_SIZE:
                    word_list.append(word)
        self.word_list = list(set(word_list))


class WordleMaxAttempts(Exception):
    pass


class WordInvalid(Exception):
    pass


class Wordle:

    _block_map = {
        "right_place": "\U0001f7e9",
        "wrong_place": "\U0001f7e8",
        "unused": "\U00002b1c",
    }
    _fore_color_map = {
        "right_place": Fore.GREEN,
        "wrong_place": Fore.YELLOW,
        "unused": Fore.BLACK,
    }

    def __init__(self, target_word, dictionary_path):
        self.target_word = target_word
        dictionary = Dictionary(dictionary_path)
        self.word_list = dictionary.word_list
        assert target_word in self.word_list
        self._num_attempts = 0
        self._tried_words = []

    def get_num_attempts(self):
        return self._num_attempts

    def play(self, trial_word):
        if self._num_attempts >= NUM_ATTEMPTS:
            raise WordleMaxAttempts
        if len(trial_word) != WORD_SIZE or (trial_word not in self.word_list):
            raise WordInvalid
        letter_map = ["unused"] * WORD_SIZE
        identified_positions = []
        for i in range(WORD_SIZE):
            if trial_word[i] == self.target_word[i]:
                letter_map[i] = "right_place"
                identified_positions.append(i)
        other_letters = [
            x for i, x in enumerate(self.target_word) if i not in identified_positions
        ]
        for i in range(WORD_SIZE):
            if (trial_word[i] in other_letters) and (letter_map[i] == "unused"):
                letter_map[i] = "wrong_place"
        self._num_attempts += 1
        self._tried_words.append((trial_word, letter_map))
        return letter_map

    def display_output(self, trial_word, letter_map):
        colored_word = ""
        for letter, status in zip(trial_word, letter_map):
            color = self._fore_color_map[status]
            colored_word += color + letter
        print(colored_word)
        print(Style.RESET_ALL)

    def display_summary(self):
        for _, letter_map in self._tried_words:
            print("".join([self._block_map[x] for x in letter_map]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--dictionary_path", required=True, help="Path to dictionary file"
    )
    args = parser.parse_args()
    target_word = getpass.getpass("Which word do you want a wordle for?:")
    game = Wordle(target_word, args.dictionary_path)
    print("Please keep attempting with 5-letter words without a prompt")
    while True:
        trial_word = getpass.getpass("")
        try:
            output_list = game.play(trial_word)
            game.display_output(trial_word, output_list)
            if set(output_list) == set(["right_place"]):
                print("You won!")
                break
        except WordInvalid:
            print(Back.BLACK + Fore.WHITE + trial_word)
            print(Style.RESET_ALL)
        except WordleMaxAttempts:
            print("Game Over!")
            break
    game.display_summary()
