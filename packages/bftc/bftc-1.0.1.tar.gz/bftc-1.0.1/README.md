# 🧠 Brainfuck to C transpiler

```python
from bftc import code_generator, tokenizer


with open("code.bf") as bf_source:
    tokens = [tokenizer.tokenize(char) for char in bf_source.read()]
    with open("code.c", "w") as c_source:
        c_source.write(code_generator.generate(tokens))

```

## Modules

- `tokens` — contain all tokens
- `tokenizer` — contain `tokenize` function

```python
def tokenize(char: str) -> Token: ...
```

- `transpiler` — contain `transpile` function

```python
def transpile(token: Token) -> str: ...
```

- `code_generator` — contain `generate` function that generate valid C code from given tokens

```python
def generate(list[Token]) -> str: ...
```

## Install
```bash
pip install bftc
```
