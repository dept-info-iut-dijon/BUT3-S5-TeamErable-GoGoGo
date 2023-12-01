from .Vector2 import Vector2

class GoConstants:
    '''Constantes du jeu de Go.'''
    Neighbors = [
        Vector2(1, 0),
        Vector2(-1, 0),
        Vector2(0, 1),
        Vector2(0, -1),
    ]

    Corners = [
        Vector2(1, 1),
        Vector2(-1, 1),
        Vector2(1, -1),
        Vector2(-1, -1),
    ]

    AllowPlayInDeadZones = False
