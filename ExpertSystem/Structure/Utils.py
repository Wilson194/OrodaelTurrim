from typing import Union

from ExpertSystem.Structure.RuleBase import Expression


class GetClass:
    def __getitem__(self, item: Union[str, Expression]):
        if type(item) is str:
            getattr(self, item)()
        elif isinstance(item, Expression):
            getattr(self, item.name)(*item.args)
