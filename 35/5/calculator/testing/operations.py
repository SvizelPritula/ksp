from dataclasses import dataclass
from typing import Iterator, List


@dataclass
class Operation:
    operation: str
    operand: int

    def eval(self, value: int) -> int:
        if self.operation == '+':
            return value + self.operand
        if self.operation == '-':
            return value + self.operand
        if self.operation == '*':
            return value * self.operand
        if self.operation == '/':
            return value // self.operand

    def __str__(self) -> str:
        return f"{self.operation}{self.operand}"


@dataclass
class Expression:
    initial: int
    operations: List[Operation]

    def eval(self) -> int:
        value = self.initial

        for op in self.operations:
            value = op.eval(value)

        return value

    def clone(self):
        return Expression(self.initial, self.operations.copy())

    def __str__(self) -> str:
        return f"{self.initial}{''.join((str(op) for op in self.operations))}"


def iter_initial() -> Iterator[Expression]:
    for i in range(10):
        yield Expression(i, [])


def iter_operations() -> Iterator[Operation]:
    for op in ['+', '-', '*', '/']:
        for i in range(10):
            if op == '/' and i == 0:
                continue

            yield Operation(op, i)
