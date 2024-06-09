
# Posibly Turn This to an Interface
class Checker:
    def check_output(actual_output: str, expected_output: str) -> bool:
        """
        Compare the actual output with the expected output.
        Returns True if they match, otherwise False.
        """
        return actual_output.strip() == expected_output.strip()
