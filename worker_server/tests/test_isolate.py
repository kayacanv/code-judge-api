import pytest
# Replace 'your_module' with the actual module name containing Isolate
from worker_server.Isolate import Isolate
from worker_server.utils.IsolateHelpers import RunStatus


@pytest.fixture
def isolate_instance():
    return Isolate()


def test_successful_cpp_execution(isolate_instance):
    cpp_code = """
    #include <iostream>
    using namespace std;
    int main() {
        cout << "HELLOO" << endl;
        return 0;
    }
    """
    result = isolate_instance.run_code(cpp_code)

    assert result.status == RunStatus.SUCCESS
    assert result.output == 'HELLOO\n'
    assert result.exitcode == 0


def test_cpp_compilation_failure(isolate_instance):
    cpp_code = """
    #include <iostream>
    using namespace std;
    int main() {
        cout << "HELLOO"
        return 0;
    }
    """  # Note the missing semicolon to induce a compilation error

    result = isolate_instance.run_code(cpp_code)

    assert result.status == RunStatus.COMPILE_ERROR


def test_cpp_runtime_error(isolate_instance):

    cpp_code = """
    #include <iostream>
    using namespace std;
    int main() {
        int a[4];
        a[-100000] = 0; // Out of bounds access
        return 0;
    }
    """

    result = isolate_instance.run_code(cpp_code)
    assert result.status == RunStatus.RUNTIME_ERROR
