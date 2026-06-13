from typing import Optional, List, Tuple
from models import TreeNode, Node, Leaf
class GameEngine:
    """движок игры: управляет текущим узлом, историей ответов, обучением"""

    def __init__(self, root: TreeNode):
        """конструктор движка"""
        self.root = root
        self.current_node: TreeNode = root  # устанавливает текущий узел на корень
        self.history: List[Tuple[Node, str]] = []  # создаёт пустой список для хранения истории (родительский узел, направление)

    def start(self):
        """начинает новую игру"""
        self.current_node = self.root  # сбрасывает текущий узел на корень
        self.history.clear()

    def get_question(self) -> Optional[str]:
        """возвращает текст вопроса или none"""
        return self.current_node.question if isinstance(self.current_node, Node) else None

    def get_guess(self) -> Optional[Tuple[str, str]]:
        """возвращает кортеж (животное, факт) или none"""
        return (self.current_node.animal, self.current_node.fact) if isinstance(self.current_node, Leaf) else None

    def answer(self, response: str):
        """обрабатывает ответ пользователя"""
        if not isinstance(self.current_node, Node):
            return
        if response == "yes":
            self.history.append((self.current_node, "yes"))
            self.current_node = self.current_node.yes
        elif response == "no":  # если ответ "нет"
            self.history.append((self.current_node, "no"))
            self.current_node = self.current_node.no

    def go_back(self) -> bool:
        """откатывает игру на один вопрос назад"""
        if not self.history:
            return False
        self.history.pop()
        self.current_node = self.history[-1][0] if self.history else self.root
        return True

    def learn_new_animal(self, correct_animal: str, new_question: str,
                         answer_for_new: str, fact: str):
        """обучает бота новому животному"""
        old_leaf = self.current_node  # сохраняет текущий лист (неправильное предположение)
        if not isinstance(old_leaf, Leaf):  # проверяет, что текущий узел - лист
            raise RuntimeError("current node must be a leaf for learning")

        new_leaf = Leaf(correct_animal, fact)  # создаёт новый лист с правильным животным

        if answer_for_new == "yes":  # если для нового животного правильный ответ "да"
            yes_child, no_child = new_leaf, old_leaf
        else:
            yes_child, no_child = old_leaf, new_leaf

        new_node = Node(new_question, yes_child, no_child)  # создаёт новый узел с вопросом и двумя ветками

        self.history.clear()  # очищает историю (начинает новую игру)
        self.current_node = self.root  # сбрасывает текущий узел на корень

