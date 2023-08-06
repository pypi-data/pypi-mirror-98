from pampy import _, match

from .tokens import (DecrementCellValueToken, GetCellValueToken,
                     IncrementCellValueToken, LoopEndToken, LoopStartToken,
                     NextCellToken, PreviousCellToken, PutCellValueToken,
                     Token)


def transpile(token: Token) -> str:
    """Transpile given token to C

    Args:
        token (Token): BF token

    Returns:
        str: C code
    """
    return match(token,
        NextCellToken, "i++;",
        PreviousCellToken, "i--;",
        PutCellValueToken, "putchar(arr[i]);",
        GetCellValueToken, "arr[i] = getchar();",
        LoopStartToken, "while(arr[i]) {",
        LoopEndToken, "}",
        IncrementCellValueToken, "arr[i]++;",
        DecrementCellValueToken, "arr[i]--;",
        _, ""
    )


__all__ = ["transpile"]
