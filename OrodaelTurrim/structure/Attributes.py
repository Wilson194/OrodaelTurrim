class AttributeBundle:
    def __init__(self, attack: float, defense: float, hit_points: float, move_range: int, sight: int, actions: int = 0):
        self.actions = actions
        self.attack = attack
        self.defense = defense
        self.hit_points = hit_points
        self.move_range = move_range
        self.sight = sight
