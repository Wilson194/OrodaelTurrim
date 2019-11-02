from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING, Any, Set, Union, Dict
from collections import deque

from ExpertSystem.Structure.Enums import LogicalOperator
from ExpertSystem.Structure.RuleBase import Rule, Expression, Fact
from OrodaelTurrim.Business.Interface.Player import IPlayer, PlayerTag
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameControlProxy, GameUncertaintyProxy
import inspect

from OrodaelTurrim.Structure.Exceptions import BadActionBaseParameters

if TYPE_CHECKING:
    from User.ActionBase import ActionBase


class IKnowledgeBase(ABC):
    """ Abstract class for User knowledge base definition """


    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy,
                 game_uncertainty_proxy: GameUncertaintyProxy, player: PlayerTag):
        self.map_proxy = map_proxy
        self.game_object_proxy = game_object_proxy
        self.game_uncertainty_proxy = game_uncertainty_proxy
        self.player = player


    @abstractmethod
    def create_knowledge_base(self) -> List[Fact]:
        """
        This method will be called every time before inference. This method should return List of created Facts
        """
        pass


class IInference(ABC):
    """ Abstract class for inference """


    @abstractmethod
    def infere(self, knowledge_base: Set[Any], rules: List[Rule], action_base: "ActionBase") -> None:
        """
        Inference method

        :param knowledge_base: - knowledge base created in the KnowledgeBase class by user
        :param rules: - parsed rules from rules file
        :param action_base: - instance of User defined action base
        """
        pass


class IActionBase(ABC):
    """
    Abstract method for user defined action base

    You can use `in` operator to check if method is in base (str or Expression)

    You can use ``[]`` operator to call function from ActionBase (with str without argument or Expresion with arguments)
    """


    def __init__(self, game_control_proxy: GameControlProxy, map_proxy: MapProxy, player: Union[IPlayer, PlayerTag]):
        """
        Constructor of Action base

        :param game_control_proxy: proxy for user operations
        :param player: Instance of your player
        """
        self.game_control_proxy = game_control_proxy
        self.map_proxy = map_proxy
        self.player = player


def get_data_holder_facts(rules: List[Rule], facts: List[Fact]) -> Dict[str, Fact]:
    """
    Get list of facts, that are marked as data holder.

    :param rules: list of rules
    :param facts: list of facts from KnowledgeBase
    :return: Dictionary (name of fact, fact object)
    """
    data_process = deque([rule.condition for rule in rules])

    fact_dictionary = {}
    for fact in facts:
        fact_dictionary[fact.name] = fact

    data_holder_facts = {}
    while data_process:
        current = data_process.pop()
        if current.operator in (LogicalOperator.AND, LogicalOperator.OR):
            data_process.append(current.left)
            data_process.append(current.right)
        elif isinstance(current.value, Expression):
            if current.value.data_holder_mark and current.value.name in fact_dictionary:
                data_holder_facts[current.value.name] = fact_dictionary[current.value.name]

    return data_holder_facts


def get_actions_with_data_holder_parameter(data_holder_facts: Dict[str, Fact], rules: List[Rule]) -> Dict[str, Set]:
    """
    Get list of actions, that have data holder parameter ( parameter with same name as data holder fact)

    :param data_holder_facts: Dictionary of data holder Facts
    :param rules: List of rules
    :return: Dictionary of action from ActionBase, which have data holder fact parameter
    """
    data_process = deque([rule.conclusion for rule in rules])

    keys = set(data_holder_facts.keys())

    actions = {}

    while data_process:
        current = data_process.pop()
        if current.operator == LogicalOperator.AND:
            data_process.append(current.left)
            data_process.append(current.right)
        elif isinstance(current.value, Expression):
            data_holder_parameters = set(current.value.args).intersection(keys)
            if data_holder_parameters:
                actions[current.value.name] = data_holder_parameters

    return actions


def check_method_parameters(method_parameters: inspect.FullArgSpec, parameters_injection: List[str],
                            function_name: str) -> bool:
    """
    Check, if data parameters could be injected without conflict

    :param method_parameters: Full argument specification of method
    :param parameters_injection: List of names of parameters, that should be injected
    :param function_name: Name of the function
    :return: True if parameters could be injected, raise Exception otherwise
    """
    if method_parameters.varkw is not None:
        return True

    for parameter in parameters_injection:
        if parameter in method_parameters.args:
            for i in range(method_parameters.args.index(parameter) + 1, len(method_parameters.args)):
                if method_parameters.args[i] not in parameters_injection:
                    raise BadActionBaseParameters(
                        f'ActionBase method "{function_name}" has position argument "{method_parameters.args[i]}" after injected argument "{parameter}"')
        elif parameter in method_parameters.kwonlyargs:
            pass
        else:
            raise BadActionBaseParameters(f'ActionBase method "{function_name}" has no "{parameter}" argument')

    return True


def create_virtual_function(target_method, parameter_to_inject):
    def virtual_function(*args, **kwargs):
        target_method(*args, **dict(parameter_to_inject, **kwargs))


    return virtual_function


class ActionBaseCaller:
    def __init__(self, facts: List[Fact], action_base: IActionBase, rules: List[Rule]):
        self.__data_holder_parameters = []
        self.__create_callable(facts, action_base, rules)
        del action_base
        del facts


    def __create_callable(self, facts: List[Fact], action_base: IActionBase, rules: List[Rule]) -> None:
        """
        Create same methods as ActionBase with injected parameters

        :param facts: List of Facts
        :param action_base: User ActionBase implementation object
        :param rules: list of rules
        """
        data_holder_facts = get_data_holder_facts(rules, facts)
        self.__data_holder_parameters = list(data_holder_facts.keys())
        target_actions = get_actions_with_data_holder_parameter(data_holder_facts, rules)

        for name, method in inspect.getmembers(action_base, predicate=inspect.ismethod):
            if not name.startswith('_'):
                if name in target_actions:
                    parameters_injection = {}
                    for parameter_name in target_actions[name]:
                        parameters_injection[parameter_name] = data_holder_facts[parameter_name].data

                    check_method_parameters(inspect.getfullargspec(method), list(parameters_injection.keys()), name)

                    setattr(self, name, create_virtual_function(method, parameters_injection))
                else:
                    setattr(self, name, method)


    def call(self, method: Union[str, Expression]) -> None:
        """
        Call method from action base. You can define method with string name or Expression object.
        With string name, you cannot pass the parameters.
        With Expression object, parameters are passed automatically.

        :param method: string name or expression node defining Action
        """
        if type(method) is str:
            getattr(self, method)()
        elif isinstance(method, Expression):
            parameters = [parameter for parameter in method.args if parameter not in self.__data_holder_parameters]
            getattr(self, method.name)(*parameters)
        else:
            raise ValueError('Get functions only by string of Expression')


    def has_method(self, method: Union[str, Expression]) -> bool:
        """
        This method check, if ActionBase contains given method.
        You can define method with string name or Expression object.

        :param method: string name or expression node defining Action
        :return: True if method exists, False otherwise
        """
        return self.__contains__(method)


    def __contains__(self, item: Union[str, Expression]) -> bool:
        if type(item) is str:
            if callable(getattr(self, item, None)):
                return True
            return False

        elif isinstance(item, Expression):
            if callable(getattr(self, item.name, None)):
                return True
            return False

        raise ValueError('Test only with string or Expression')
