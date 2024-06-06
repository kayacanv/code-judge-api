import random
import subprocess
from utils.IsolateHelpers import RunResult, RunStatus


class Isolate:
    def __init__(self):
        self.box_id = str(random.randint(0, 999))  # TODO: Revise this logic
        self.base_path = self._init_sandbox()
        self.run_path = f"{self.base_path}/box"
        self.meta_path = f"{self.run_path}/meta.txt"
        self.metadata = {}
        print(f'base_path => {self.base_path}')

    def _run_command(self, command, fail_on_exception=False):
        result = subprocess.run(command, shell=True,
                                capture_output=True, text=True)
        if fail_on_exception and result.returncode != 0:
            raise Exception(f"Failed run command: {result.stderr}")
        return result

    def _init_sandbox(self):
        command = f"isolate --box-id={self.box_id} --init"
        result = self._run_command(command, True)
        return result.stdout.strip()

    def __del__(self):
        command = f"isolate --box-id={self.box_id} --cleanup"
        self._run_command(command)

    def _write_code_to_file(self, code, file_extension='cpp'):
        # Write code to file
        with open(f"{self.run_path}/code.{file_extension}", "w") as code_file:
            code_file.write(code)

    def _compile_code(self):
        result = self._run_command(
            f'isolate -p --box-id={self.box_id} -E PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --run -- /usr/bin/g++ code.cpp -o code'
        )
        return result.returncode == 0

    def _run_code(self):
        # --stderr-to-stdout
        return self._run_command(f'isolate -p --box-id={self.box_id} --stderr-to-stdout --meta={self.meta_path} -E PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --run -- ./code')

    def metadata_parser(self):
        metrics = {}

        with open(self.meta_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                # Remove any surrounding whitespace and split by colon
                key, value = line.strip().split(':')
                # Store the key-value pair in the dictionary
                metrics[key] = value

        self.metadata = metrics

    def run_code(self, code) -> RunResult:
        self._write_code_to_file(code)
        compile_success = self._compile_code()
        if compile_success:
            run_code_status = self._run_code()
        self.metadata_parser()
        return RunResult(
            RunStatus.getRunStatus(
                compile_success,
                RunStatus.SUCCESS if run_code_status.returncode == 0
                else RunStatus.RUNTIME_ERROR
            ),
            run_code_status.stdout,
            self.metadata,
            run_code_status.stderr,
            run_code_status.returncode,
        )


# Example usage
if __name__ == "__main__":
    isolate = Isolate()
    python_code = """
        print("HEY THIS IS PYTHON")
    """
    cpp_code = """
        #include <iostream>
        using namespace std;
        int main() {
            int a[4];

            cout << "HELLOO" << endl;
            return 0;
        }
    """
    input_data = "Hello, world!"
#    python_output = isolate.run_code(python_code, input_data, "python")
    cpp_output = isolate.run_code(cpp_code)
#   print("Python Output:", python_output)
    cpp_output.printResult()
    print(isolate.metadata)
