from dmoj.executors.CPP03 import Executor as CPPExecutor
from typing import List


class Executor(CPPExecutor):
    command = 'g++_ACL'
    command_paths = ['g++-11', 'g++']
    std = 'c++20'
    test_program = """
#include <iostream>

int main() {
    std::strong_ordering comparison = 1 <=> 2;
    auto input = std::cin.rdbuf();
    std::cout << input;
    return 0;
}
"""

    def get_defines(self) -> List[str]:
        return ['-I', '/usr/include/ac-library'] + super().get_defines()