class Expression:
    def __init__(self):
        self.name = None
        self.args = []
        self.comparator = None
        self.value = None

    def evaluate(self):
        pass

    def __repr__(self):
        if self.comparator is None:
            return '{} {}'.format(self.name, ' '.join(self.args))
        else:
            return '{} {} {} {}'.format(self.name, ' '.join(self.args), self.comparator, self.value)


class ExpressionNode:
    def __init__(self):
        self.left = None
        self.right = None
        self.value = None
        self.parent = None
        self.parentheses = False

    def __repr__(self):
        if self.left:
            if self.parentheses:
                return '({} {} {})'.format(self.left.__repr__(), self.value, self.right.__repr__())
            else:
                return '{} {} {}'.format(self.left.__repr__(), self.value, self.right.__repr__())
        else:
            return self.value


class ExpressionTree:
    def __init__(self, root: ExpressionNode):
        self.root = root

    def __repr__(self):
        return self.root.__repr__()


class Rule:
    def __init__(self):
        self.condition = None
        self.conclusion = None

    def __repr__(self):
        return 'IF {} THEN {}'.format(self.condition.__repr__(), self.conclusion.__repr__())
