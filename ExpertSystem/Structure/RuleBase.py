from typing import Union, List, Callable


class Expression:
    """Class that represent one expression"""


    def __init__(self):
        self.__name = None
        self.__args = []
        self.__comparator = None
        self.__value = None
        self.__uncertainty = None


    @property
    def name(self) -> str:
        """Name of the expression"""
        return self.__name


    @name.setter
    def name(self, value: str):
        self.__name = value


    @property
    def args(self) -> List[str]:
        """List of expression arguments"""
        return self.__args


    @args.setter
    def args(self, value: List[str]):
        self.__args = value


    @property
    def comparator(self) -> str:
        """Comparator between expression and value (<, >, <=, >=, ==, !=)"""
        return self.__comparator


    @comparator.setter
    def comparator(self, value: str):
        self.__comparator = value


    @property
    def value(self):
        """ Value of constant"""
        return self.__value


    @value.setter
    def value(self, value):
        self.__value = value


    @property
    def uncertainty(self):
        return self.__uncertainty


    @uncertainty.setter
    def uncertainty(self, value):
        self.__uncertainty = value


    def evaluate(self):
        pass


    def __repr__(self):
        text = ''
        text += '{} {}'.format(self.name, ' '.join(self.args))
        if self.comparator:
            text += '{} {}'.format(self.comparator, self.value)

        if self.uncertainty:
            text += '[{}]'.format(self.uncertainty)
        return text


class ExpressionNode:
    """One node in tree representing logical expression"""


    def __init__(self):
        self.__left = None
        self.__right = None
        self.__value = None
        self.__parent = None
        self.__parentheses = False


    @property
    def left(self) -> Union["ExpressionNode", None]:
        """Left child of the Node"""
        return self.__left


    @left.setter
    def left(self, value: Union["ExpressionNode"]):
        self.__left = value


    @property
    def right(self) -> Union["ExpressionNode", None]:
        """Right child of the Node"""
        return self.__right


    @right.setter
    def right(self, value: Union["ExpressionNode"]):
        self.__right = value


    @property
    def value(self) -> Union[Expression, str, None]:
        """
        Value of the node
            str -> logical operator for left and right Nodes

            Expression  -> left and right nodes are None
        """
        return self.__value


    @value.setter
    def value(self, value: Union[Expression, str]):
        self.__value = value


    @property
    def parent(self) -> Union["ExpressionNode", None]:
        """Parent of the node"""
        return self.__parent


    @parent.setter
    def parent(self, value: "ExpressionNode"):
        self.__parent = value


    @property
    def parentheses(self) -> bool:
        """True if current level of expression have parentheses"""
        return self.__parentheses


    @parentheses.setter
    def parentheses(self, value: bool):
        self.__parentheses = value


    def __repr__(self):
        if self.left:
            if self.parentheses:
                return '({} {} {})'.format(self.left.__repr__(), self.value, self.right.__repr__())
            else:
                return '{} {} {}'.format(self.left.__repr__(), self.value, self.right.__repr__())
        else:
            return self.value.__repr__()


class Rule:
    """
    Class for store one rule
    """


    def __init__(self):
        self.__condition = None
        self.__conclusion = None
        self.__uncertainty = None


    @property
    def condition(self) -> ExpressionNode:
        """Condition of the rule"""
        return self.__condition


    @condition.setter
    def condition(self, value):
        self.__condition = value


    @property
    def conclusion(self) -> ExpressionNode:
        """Conclusion of the rule"""
        return self.__conclusion


    @conclusion.setter
    def conclusion(self, value):
        self.__conclusion = value


    @property
    def uncertainty(self):
        return self.__uncertainty


    @uncertainty.setter
    def uncertainty(self, value):
        self.__uncertainty = value


    def __repr__(self):
        if self.uncertainty:
            return 'IF {} THEN {} WITH {}'.format(self.condition.__repr__(), self.conclusion.__repr__(), self.uncertainty)
        else:
            return 'IF {} THEN {}'.format(self.condition.__repr__(), self.conclusion.__repr__())


class Fact:
    def __init__(self, name: str, eval_function: Callable = None, probability: float = 1):
        self.name = name
        self.probability = probability
        if eval_function:
            self.evaluate = eval_function


    def evaluate(self, *args, **kwargs):
        return True


    def __call__(self, *args, **kwargs):
        return self.evaluate(*args, **kwargs)


    def __hash__(self):
        return hash(self.name)


    def __eq__(self, other):
        return self.name == other
