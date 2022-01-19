import collections
from wordle import Wordle, WORD_SIZE, WordleMaxAttempts


class PlayWordle:
    def __init__(self, game_object):
        self.game_object = game_object
        self.word_list = game_object.word_list
        self.letters_to_be_used = set()
        self.right_place_letters = {}
        self.wrong_place_letters = {i: set() for i in range(WORD_SIZE)}

    def print_state(self):
        var_dict = dict(vars(self))
        var_dict["word_list"] = None
        var_dict["short_list"] = len(var_dict["short_list"])
        var_dict["game_object"] = var_dict["game_object"].get_num_attempts()
        print("\nSolver state: {}".format(var_dict))

    @staticmethod
    def get_word_score_unordered(word, letter_count):
        return sum([letter_count.get(x, 0) for x in set(word)])

    @staticmethod
    def get_word_score_ordered(word, ordered_letter_counts):
        return sum([ordered_letter_counts[i][x] for i, x in enumerate(word)])

    def get_overlap(self, word):
        score = 0
        for short_word in self.short_list:
            for x in set(word):
                if (x not in self.letters_to_be_used) and (x in short_word):
                    score += 1
                    break
        return score

    def get_best_word_ordered(self, word_list, letter_count, ordered_letter_counts):
        score_list = [
            (
                PlayWordle.get_word_score_ordered(word, ordered_letter_counts)
                + WORD_SIZE * PlayWordle.get_word_score_unordered(word, letter_count),
                word,
            )
            for word in word_list
        ]
        sorted_list = sorted(score_list)
        if (sorted_list[-1][0] / sorted_list[-10][0] - 1) < 1e-4:
            # need a tie-breaker!
            highest_score = sorted_list[-1][0]
            candidates = [
                y for (x, y) in sorted_list[-5:] if (highest_score / x - 1 < 1e-4)
            ]
            new_scores = [(self.get_overlap(y), y) for y in candidates]
            sorted_list = sorted(new_scores)
        return sorted_list[-1]

    def is_word_valid(self, word):
        if not all([(x in word) for x in self.letters_to_be_used]):
            return False
        for index in range(len(word)):
            if (index in self.right_place_letters) and (
                self.right_place_letters[index] != word[index]
            ):
                return False
            if word[index] in self.wrong_place_letters[index]:
                return False
        return True

    def get_unordered_letter_weight(self, word_list):
        unordered_letter_count = collections.Counter("".join(word_list))
        total_weight = len(word_list)
        unordered_letter_weight = {}
        alphabet_length = len(unordered_letter_count)
        for key in unordered_letter_count:
            unordered_letter_weight[key] = max(
                0.0,
                unordered_letter_count[key]
                * 1.0
                * (total_weight - unordered_letter_count[key])
                / (total_weight ** 2),
            )
        return unordered_letter_weight

    def get_ordered_letter_weight(self, word_list):
        ordered_letter_counts = {}
        for i in range(WORD_SIZE):
            ordered_letter_counts[i] = collections.Counter([x[i] for x in word_list])
            for j in ordered_letter_counts[i]:
                total_weight = len(word_list)
                ordered_letter_counts[i][j] = (
                    ordered_letter_counts[i][j]
                    * 1.0
                    * (total_weight - ordered_letter_counts[i][j])
                    / (total_weight ** 2)
                )
        return ordered_letter_counts

    def play(self, debug=False):
        self.short_list = self.word_list[:]
        styles = []
        while True:
            if debug:
                self.print_state()
                print("We are now at {} shortlisted words".format(len(self.short_list)))
            try:
                if len(self.short_list) <= 2:
                    word_choice = self.short_list[0]
                    styles.append("guess")
                else:
                    unordered_letter_weight = self.get_unordered_letter_weight(
                        self.short_list
                    )
                    ordered_letter_counts = self.get_ordered_letter_weight(
                        self.short_list
                    )
                    score, word_choice = self.get_best_word_ordered(
                        self.word_list,
                        unordered_letter_weight,
                        ordered_letter_counts,
                    )
                    styles.append("simple")
                    if debug and (len(self.short_list) < 40):
                        print(
                            "The short-listed words are: {}".format(
                                ", ".join(self.short_list)
                            )
                        )

                op = self.game_object.play(word_choice)
                if debug:
                    print(
                        f"The solver chose '{word_choice}' with score {score} and got output {op}"
                    )
                if set(op) == set(["right_place"]):
                    return (True, word_choice, styles)
                for i, s in enumerate(op):
                    if s in ("wrong_place", "right_place"):
                        self.letters_to_be_used.add(word_choice[i])
                        if s == "right_place":
                            self.right_place_letters[i] = word_choice[i]
                            self.wrong_place_letters[i] = set()
                        elif i not in self.right_place_letters:
                            self.wrong_place_letters[i].add(word_choice[i])
                for i, s in enumerate(op):
                    if s == "unused":
                        for j in range(WORD_SIZE):
                            if word_choice[i] != self.right_place_letters.get(
                                j, None
                            ) and (j not in self.right_place_letters):
                                self.wrong_place_letters[j].add(word_choice[i])
                self.short_list = [
                    word for word in self.short_list if self.is_word_valid(word)
                ]
            except WordleMaxAttempts:
                return (False, None, styles)


if __name__ == "__main__":
    game = Wordle("roker", "unix_words.txt")
    passed, word, styles = PlayWordle(game).play(debug=True)
    print((passed, word, styles, game.get_num_attempts()))
