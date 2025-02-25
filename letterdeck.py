
import random

class LetterDeck:
    # Original relative frequencies (proportions) for the letters.
    LETTER_FREQUENCIES = {
        'A': 0.08, 'B': 0.0175, 'C': 0.034, 'D': 0.0405,
        'E': 0.1185, 'F': 0.018, 'G': 0.025, 'H': 0.042,
        'I': 0.078, 'J': 0.0018, 'K': 0.0087, 'L': 0.0465,
        'M': 0.0255, 'N': 0.0695, 'O': 0.068, 'P': 0.0235,
        'Q': 0.001425, 'R': 0.0665, 'S': 0.075, 'T': 0.079,
        'U': 0.0305, 'V': 0.0099, 'W': 0.01655, 'X': 0.0021,
        'Y': 0.018, 'Z': 0.00257
    }
    VOWELS = set("AEIOU")

    def __init__(self, power=0.5):
        """
        Initialize the deck with adjusted frequencies using a power transformation.
        This creates three dictionaries:
            - overall normalized frequencies,
            - normalized vowels frequencies,
            - normalized consonants frequencies.
        """
        self.adjusted_frequencies = self._adjust_frequencies(power)
        self.normalized_frequencies = self._normalize_frequencies(self.adjusted_frequencies)
        # Split into vowels and consonants:
        vowel_freq = {letter: freq for letter, freq in self.adjusted_frequencies.items() if letter in self.VOWELS}
        consonant_freq = {letter: freq for letter, freq in self.adjusted_frequencies.items() if letter not in self.VOWELS}
        self.normalized_vowel = self._normalize_frequencies(vowel_freq)
        self.normalized_consonant = self._normalize_frequencies(consonant_freq)

    def _adjust_frequencies(self, power):
        """Flatten the distribution using a power transformation."""
        return {letter: (weight ** power)
                for letter, weight in self.LETTER_FREQUENCIES.items()}

    def _normalize_frequencies(self, freq_dict):
        """Normalize frequencies in freq_dict so they sum to 1."""
        total = sum(freq_dict.values())
        return {letter: weight / total for letter, weight in freq_dict.items()}

    def _pick_from_pool(self, pool, current_counts):
        """
        Generic helper: pick a letter from a given normalized pool,
        filtering out any letter that has already been chosen twice.
        """
        valid_letters = [letter for letter in pool if current_counts.get(letter, 0) < 2]
        if not valid_letters:
            raise ValueError("No valid letters available to pick.")
        valid_weights = [pool[letter] for letter in valid_letters]
        # Re-normalize valid weights.
        total = sum(valid_weights)
        normalized_valid_weights = [w / total for w in valid_weights]
        return random.choices(valid_letters, weights=normalized_valid_weights, k=1)[0]

    def pick_letter(self, current_counts):
        """
        Pick a letter from the overall pool, ensuring that no letter is picked more than twice.
        """
        return self._pick_from_pool(self.normalized_frequencies, current_counts)

    def pick_vowel(self, current_counts):
        """
        Pick a vowel from the vowel pool, ensuring that no vowel is picked more than twice.
        """
        return self._pick_from_pool(self.normalized_vowel, current_counts)

    def pick_consonant(self, current_counts):
        """
        Pick a consonant from the consonant pool, ensuring that no consonant is picked more than twice.
        """
        return self._pick_from_pool(self.normalized_consonant, current_counts)

    def generate_letters(self, n=9):
        """
        Generate n letters using the overall distribution one-by-one.
        This does not let the player choose vowel vs. consonant.
        """
        letters = []
        counts = {}
        for _ in range(n):
            letter = self.pick_letter(counts)
            letters.append(letter)
            counts[letter] = counts.get(letter, 0) + 1
        return letters

    def generate_letters_by_choice(self, vowel_count, consonant_count):
        """
        Generate a set of letters with a pre-defined number of vowels and consonants.
        The order of letters is then randomized.
        """
        if vowel_count + consonant_count <= 0:
            raise ValueError("Total letters must be positive.")
        letters = []
        counts = {}
        # Pick vowels.
        for _ in range(vowel_count):
            letter = self.pick_vowel(counts)
            letters.append(letter)
            counts[letter] = counts.get(letter, 0) + 1
        # Pick consonants.
        for _ in range(consonant_count):
            letter = self.pick_consonant(counts)
            letters.append(letter)
            counts[letter] = counts.get(letter, 0) + 1
        random.shuffle(letters)
        return letters

if __name__ == "__main__":
    deck = LetterDeck(power=0.5)
    counts = {}
    chosen_letters = []
    target_count = 9

    print("Welcome to the Countdown Letter Picker!")
    print("You will choose 9 letters by specifying 'vowel' or 'consonant' each time.")
    print("Note: No letter can appear more than twice.\n")

    while len(chosen_letters) < target_count:
        print("Current letters:", " ".join(chosen_letters))
        choice = input("Choose (v)owel or (c)onsonant: ").strip().lower()

        # Validate the input
        if choice not in ("v", "c"):
            print("Invalid input. Please type 'v' for vowel or 'c' for consonant.\n")
            continue

        try:
            if choice == "v":
                letter = deck.pick_vowel(counts)
            else:  # choice == "c"
                letter = deck.pick_consonant(counts)
            chosen_letters.append(letter)
            counts[letter] = counts.get(letter, 0) + 1
            print(f"You picked: {letter}\n")
        except ValueError as e:
            print("Error:", e)
            continue

    print("Final set of letters:", " ".join(chosen_letters))