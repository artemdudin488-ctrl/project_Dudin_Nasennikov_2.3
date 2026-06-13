from __future__ import \
    annotations  # позволяет использовать TreeNode как ссылку на текущий модуль внутри аннотаций типов
from typing import Union

class Leaf:
    """лист дерева - конечный узел, содержащий животное и факт о нём"""

    def __init__(self, animal: str, fact: str):
        self.animal = animal  # сохраняет название животного в атрибут экземпляра
        self.fact = fact

class Node:
    """узел дерева - содержит вопрос и две ветки: да и нет"""

    def __init__(self, question: str, yes: TreeNode, no: TreeNode):
        self.question = question
        self.yes = yes
        self.no = no

TreeNode = Union[Node, Leaf]  # определяет объединённый тип: узел дерева может быть Node или Leaf