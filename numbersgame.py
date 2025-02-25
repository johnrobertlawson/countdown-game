"""Countdown Numbers Game
"""

import os
import time

import numpy as np

class NumbersGame:
    def __init__(self, numbers=None, target=None, timer=45):
        """Numbers game class for the Countdown game.

        TODO: if numbers or target is none, generate
        """
        self.rng = np.random.default_rng()  # Create RNG instance
        self.numbers = numbers if (numbers is not None
                        ) else self.generate_numbers(target=False)
        self.target = target if (target is not None
                        ) else self.generate_numbers(numbers=False)
        self.timer = timer

    def generate_numbers(self, target=True, numbers=True):
        """Generate numbers and target for the game.

        Args:
            target (bool): Generate target number
            numbers (bool): Generate number set
        """
        target_val = self.generate_target() if target else None
        numbers_val = self.generate_number_set() if numbers else None
        return numbers_val, target_val

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

    def solve_numbers(self):
        """Find a sequence of operations that uses the numbers to reach the target."""
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

        return helper(self.numbers, [])

    def start_round(self):
        self.numbers, self.target = self.generate_numbers()

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

    def provide_solution(self):
        return self.solve_numbers()

    def lookup_points_awarded(self, answer):
        """Lookup points awarded based on distance from target.
        """
        distance = abs(answer - self.target)
        if distance == 0:
            return 10
        elif distance <= 5:
            return 7
        elif distance <= 10:
            return 5
        elif distance <= 20:
            return 3
        else:
            return 0


# -------------------------
# Testing the solve_numbers function
# -------------------------
if __name__ == "__main__":
    NG = NumbersGame()

    # Player give their methods...

    # "Genius Robot" looking for optimal answer
    solution_steps = NG.solve_numbers()

    if solution_steps:
        print("Solution found:")
        for idx, step in enumerate(solution_steps, start=1):
            print(f"Step {idx}:")
            print(f"  Expression: {step['expression']}")
            print(f"  Description: {step['description']}")
            print(f"  Available Numbers: {step['available_numbers']}\n")
    else:
        print("No solution found.")
