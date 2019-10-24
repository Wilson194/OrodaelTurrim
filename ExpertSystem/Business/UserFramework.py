from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING, Any, Set, Union

from ExpertSystem.Structure.RuleBase import Rule, Expression, Fact
from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameControlProxy, GameUncertaintyProxy

if TYPE_CHECKING:
    from User.ActionBase import ActionBase


class IKnowledgeBase(ABC):
    """ Abstract class for User knowledge base definition """


    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy,
                 game_uncertainty_proxy: GameUncertaintyProxy, player: IPlayer):
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


    def __init__(self, game_control_proxy: GameControlProxy, map_proxy: MapProxy, player: IPlayer):
        """
        Constructor of Action base

        :param game_control_proxy: proxy for user operations
        :param player: Instance of your player
        """
        self.game_control_proxy = game_control_proxy
        self.map_proxy = map_proxy
        self.player = player


    def __getitem__(self, item: Union[str, Expression]) -> None:
        if type(item) is str:
            getattr(self, item)()
        elif isinstance(item, Expression):
            getattr(self, item.name)(*item.args)
        else:
            raise ValueError('Get functions only by string of Expression')


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
