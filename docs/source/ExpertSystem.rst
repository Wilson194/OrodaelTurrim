Expert system
===================


Knowledge base
-----------------



Interference
--------------



Action base
--------------


Custom filters
------------------

In the section **TODO** you can read about move and attack filter system. Now talk about how to create own custom filters.
As a defender, you can use only attack filters, because your unit cannot move. But also some smart attack filters
could be really handy in some cases.

If you want to define you own filter, you need to create new class that inherit from
``OrodaelTurrim.Structure.Filter.FilterPattern.AttackFilter``. There are some restrictions for your filters:

 * Your filter class must be in ``AttackFilter.py`` file in ``User`` module
 * Your filter must inherit only ``OrodaelTurrim.Structure.Filter.FilterPattern.AttackFilter``
 * Your filter must overload ``filter`` method with same parameters
 * ``filter`` method must return List of tiles and tiles must be subset of given ``tiles`` List
 * You can overload ``__init__`` method but first two parameters must be same as in abstract class and you must
   call __init__ from inherited class
 * You can implement as many functions as you wont in filter class

If your class meets all requirements, you will see this filter in GUI and also you can instance your filter with
``FilterFactory`` (you can instance them directly but then you need to take care of initial parameters).

In the ``AttackFilter.py`` file you have example of custom filter.