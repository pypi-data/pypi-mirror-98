from typing import *


class Problem:
    initial = goal = None
    def __init__(self, initial: Any, goal: Any = None) -> None:
        self.initial: 'initial' = initial
        self.goal: 'initial' = goal

    def actions(self, state: 'Problem.initial') -> Any: ...

    def transition(self, state: 'Problem.initial', action: Any) -> Any: ...

    def goal_test(self, state: 'Problem.initial') -> bool: ...


class Node:
    state = parent = action = None
    def __init__(self, state: 'Problem.initial', parent: Node = None, action: Any = None) -> None:
        self.state: 'Problem.initial' = state
        self.parent: Node = parent
        self.action = action

    def __eq__(self, other: Node) -> bool: ...

    def expand(self, problem: Problem) -> list: ...

    def path(self) -> list: ...


def TreeSearch(problem: Problem) -> Node or None: ...
