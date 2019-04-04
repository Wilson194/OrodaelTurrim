from typing import List

from OrodaelTurrim.Structure.Filter.FilterPattern import AttackFilter
from OrodaelTurrim.Structure.Position import Position

""" 
In this file you can define your ow attack filters if default filters are not enough for your. 
Filter must be subclass of class `AttaclFilter` and must implement filter method with same signature

def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
    pass
    
    
You can here define as many filters as you want. Framework fill find correct filters and load them.
 
"""


class DummyAttackFilter(AttackFilter):
    """ Example of custom filter """


    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        return tiles
