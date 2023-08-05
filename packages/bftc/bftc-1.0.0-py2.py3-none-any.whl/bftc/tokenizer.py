from pampy import _, match

from .tokens import (DecrementCellValueToken, GetCellValueToken,
                     IncrementCellValueToken, InvalidSyntaxToken, LoopEndToken,
                     LoopStartToken, NextCellToken, PreviousCellToken,
                     PutCellValueToken, Token)


def tokenize(char: str) -> Token:
    return match(char,
        "+", IncrementCellValueToken(),
        "-", DecrementCellValueToken(-1),
        ".", PutCellValueToken(),
        ",", GetCellValueToken(),
        "[", LoopStartToken(),
        "]", LoopEndToken(),
        ">", NextCellToken(),
        "<", PreviousCellToken(),
        _, InvalidSyntaxToken()
    )


__all__ = ["tokenize"]
