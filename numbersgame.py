"""Countdown Numbers Game
"""

import os
import time

import numpy as np

class NumbersGame:
    def __init__(self, numbers=None, target=None, timer=45, auto_pick=False):
        """Numbers game class for the Countdown game.

        TODO: if numbers or target is none, generate
        """
        self.rng = np.random.default_rng()  # Create RNG instance
        self.timer = timer

        if numbers is not None:
            self.numbers = numbers
        else:
            if auto_pick:
                self.numbers = self.generate_number_set()
            else:
                self.numbers = []

        self.target = target if target is not None else self.generate_target()

    def generate_target(self):
        """Generate a target number between 100 and 999."""
        return self.rng.integers(100, 1000)

    def generate_number_set(self):
        """Generate the set of numbers to play with."""
        large_numbers = np.array([25, 50, 75, 100])
        small_numbers = np.repeat(np.arange(1, 11), 2)

        large_picks = self.rng.choice(large_numbers, size=1, replace=False)
        small_picks = self.rng.choice(small_numbers, size=5, replace=False)
        return np.concatenate([large_picks, small_picks])

    @staticmethod
    def get_operations():
        """Returns the valid operations for the numbers game."""
        return [
            ('+', lambda x, y: x + y, "Add"),
            ('-', lambda x, y: x - y if x - y > 0 else None, "Subtract"),
            ('*', lambda x, y: x * y, "Multiply"),
            ('/', lambda x, y: x // y if y != 0 and x % y == 0 else None, "Divide")
        ]

    def solve_numbers(self, explain=True):
        """Find a sequence of operations that uses the numbers to reach the target.

        I think it's being too complicated.
        It should rank solutions by simplicity.
        Maybe sample a subset of solutions if too long to run permutations.
        """
        def helper(current_numbers, steps):
            if self.target in current_numbers:
                return steps
            if len(current_numbers) == 1:
                return None

            for i in range(len(current_numbers)):
                for j in range(i + 1, len(current_numbers)):
                    a = current_numbers[i]
                    b = current_numbers[j]
                    remaining = [current_numbers[k] for k in range(len(current_numbers))
                                 if k != i and k != j]

                    for op, func, op_name in self.get_operations():
                        for (x, y) in [(a, b), (b, a)]:
                            result = func(x, y)
                            if result is None:
                                continue
                            new_numbers = remaining + [result]
                            expression = f"{x} {op} {y} = {result}"
                            description = f"{op_name} {x} and {y} to get {result}."
                            new_step = {
                                'expression': expression,
                                'description': description,
                                'available_numbers': new_numbers.copy()
                            }
                            solution = helper(new_numbers, steps + [new_step])
                            if solution is not None:
                                return solution
            return None

        solution = helper(self.numbers, [])

        if (solution is not None) and explain:
            print("Solution found by Genius Robot:")
            for idx, step in enumerate(solution, start=1):
                print(f"Step {idx}:")
                print(f"  Expression: {step['expression']}")
                print(f"  Description: {step['description']}")
                print(f"  Available Numbers: {[int(num) for num in step['available_numbers']]}\n")
        else:
            print("No solution found.")

        return solution

    def check_solution(self, expression):
        # Evaluate the expression safely and check if it equals target
        # TODO: see how this works in real-time with CLI then GUI
        try:
            result = eval(expression, {"__builtins__": None}, {})
            if result == self.target:
                return True, f"Correct! {expression} = {self.target}"
            else:
                return False, f"Incorrect: {expression} = {result}, target was {self.target}"
        except Exception as e:
            return False, f"Error in expression: {e}"

    def lookup_points_awarded(self, answer):
        """Lookup points awarded based on distance from target.
        """
        distance = int(abs(answer - self.target))
        if distance <= 5:
            return 10 - distance
        elif distance <= 10:
            return 4
        elif distance <= 20:
            return 2
        else:
            return 0

    def generate_human_guess(self, skill_level=0.5):
        """Generate a value mimicking human guess based on skill level.

        We assume the method is correct, for now, for simplicity.

        Returns:
            int: The guess value.
        """
        if skill_level < 0 or skill_level > 1:
            raise ValueError("Skill level must be between 0 and 1.")

        # Randomly decide if the player will be within 10 of the target
        close_guess = self.rng.random() < skill_level
        if close_guess:
            deviation = int(round(self.rng.normal(0, 2)))
            return self.target + deviation
        else:
            return self.rng.integers(1, 101)



# -------------------------
# Testing the solve_numbers function
# -------------------------
if __name__ == "__main__":
    NG = NumbersGame(auto_pick=True)

    print(f"The chosen numbers are: {NG.numbers}")
    print(f"The target is: {NG.target}.")


    # Player give their numbers
    # Assume methods are correct for now
    answer1 = NG.generate_human_guess(skill_level=0.5)
    print(f"Player 1's answer: {answer1}")
    answer2 = NG.generate_human_guess(skill_level=0.92)
    print(f"Player 2's answer: {answer2}")

    # "Genius Robot" looking for optimal answer
    NG.solve_numbers(explain=True)


    # Give the scores
    score1 = NG.lookup_points_awarded(answer1)
    score2 = NG.lookup_points_awarded(answer2)
    print(f"Player 1 scored {score1} points.")
    print(f"Player 2 scored {score2} points.")
