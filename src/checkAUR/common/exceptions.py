"""Module for custom exceptions
"""


class ProgramNotInstalledError(Exception):
    """Custom exception for situation, when program is not found
    """
    def __init__(self, program: str, *args):
        """Custom exception for situation, when program is not found

        Args:
            program (str): name of missing program
            args: standard Exception arguments
        """
        self.program = program
        self.message = f"Following program could not be launched: {program}\nProbably not installed!"
        super().__init__(self.message, args)
