from pampy import _, match

from .tokens import (DecrementCellValueToken, GetCellValueToken,
                     IncrementCellValueToken, InvalidSyntaxToken, LoopEndToken,
                     LoopStartToken, NextCellToken, PreviousCellToken,
                     PutCellValueToken, Token)


def tokenize(char: str) -> Token:
    """Tokenize given Brainfuck command

    Args:
        char (str): Brainfuck command

    Returns:
        Token: token
    """
    return match(char,
        "+", IncrementCellValueToken(),
        "-", DecrementCellValueToken(),
        ".", PutCellValueToken(),
        ",", GetCellValueToken(),
        "[", LoopStartToken(),
        "]", LoopEndToken(),
        ">", NextCellToken(),
        "<", PreviousCellToken(),
        _, InvalidSyntaxToken()
    )


__all__ = ["tokenize"]
