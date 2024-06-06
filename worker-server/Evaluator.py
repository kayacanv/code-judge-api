from Isolate import Isolate
from Checker import Checker
from utils.IsolateHelpers import RunStatus, RunResult


class Evaluator:
    def __init__(self):
        self.isolate = Isolate()

    def evaluate(self, code: str, expected_output: str) -> bool:
        # Run the code using the Isolate class
        run_result = self.isolate.run_code(code)
        if run_result.status == RunStatus.SUCCESS:
            return Checker.check_output(
                run_result.output,
                expected_output
            )
        return False


# Example usage
if __name__ == "__main__":
    evaluator = Evaluator()

    cpp_code = """
    #include <iostream>
    using namespace std;
    int main() {
        cout << "Hello, World!" << endl;
        return 0;
    }
    """
    expected_output = "Hello, World!"

    evaluation_result = evaluator.evaluate(cpp_code, expected_output)

    print(f"Status: {evaluation_result}")
