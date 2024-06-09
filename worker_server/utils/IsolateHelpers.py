from enum import Enum


class RunStatus(Enum):
    SUCCESS = "SUCCESS"
    COMPILE_ERROR = "COMPILE_ERROR"
    RUNTIME_ERROR = "RUNTIME_ERROR"

    def getRunStatus(compile_success: bool, run_code_success: bool):
        if not compile_success:
            return RunStatus.COMPILE_ERROR
        if not run_code_success:
            return RunStatus.RUNTIME_ERROR
        return RunStatus.SUCCESS


class CompileResult:
    def __init__(self, status, error=None, exitcode=None):
        self.status = status
        self.error = error
        self.exitcode = exitcode


class RunResult:
    def __init__(self, status, output=None, metadata=None,
                 error=None, exitcode=None):
        self.status = status
        self.output = output
        self.metadata = metadata
        self.error = error
        self.exitcode = exitcode

    def printResult(self):
        print('Result ==>')
        print(f'status: {self.status}')
#        print(f'output: {self.output}')
        print(f'metadata: {self.metadata}')
        print(f'error: {self.error}')
        print(f'exitcode: {self.exitcode}')
