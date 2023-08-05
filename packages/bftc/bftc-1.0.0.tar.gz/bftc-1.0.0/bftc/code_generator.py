from .tokens import Token
from .transpiler import transpile

C_CODE = """
#include <stdio.h>


int main(int argc, char **argv) {
    int i = 0;
    char arr[30000];
    memset(arr, 0, sizeof(arr));
    {}
}
"""


def generate(tokens: list[Token]) -> str:
    return C_CODE.format("\n".join([transpile(token) for token in tokens]))


__all__ = ["generate"]
