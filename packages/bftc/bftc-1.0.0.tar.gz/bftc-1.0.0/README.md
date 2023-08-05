# 🧠 Brainfuck to C transpiler

## Modules:

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
