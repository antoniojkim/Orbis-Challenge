from PythonClientAPI.game.PointUtils import *
from PythonClientAPI.game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.game.Enums import Team
from PythonClientAPI.game.World import World
from PythonClientAPI.game.TileUtils import TileUtils
from random import choice as choose_random_from

class PlayerAI:

    def __init__(self):
        ''' Initialize! '''
        self.turn_count = 0             # game turn count
        self.target = None              # target to send unit to!
        self.outbound = True            # is the unit leaving, or returning?

    def do_move(self, world, friendly_unit, enemy_units):
        '''
        This method is called every turn by the game engine.
        Make sure you call friendly_unit.move(target) somewhere here!

        Below, you'll find a very rudimentary strategy to get you started.
        Feel free to use, or delete any part of the provided code - Good luck!

        :param world: world object (more information on the documentation)
            - world: contains information about the game map.
            - world.path: contains various pathfinding helper methods.
            - world.util: contains various tile-finding helper methods.
            - world.fill: contains various flood-filling helper methods.

        :param friendly_unit: FriendlyUnit object
        :param enemy_units: list of EnemyUnit objects
        '''

        # increment turn count
        self.turn_count += 1

        # if unit is dead, stop making moves.
        if friendly_unit.status == 'DISABLED':
            print("Turn {0}: Disabled - skipping move.".format(str(self.turn_count)))
            self.target = None
            self.outbound = True
            return

        def viable(tile):
            if tile.is_wall or tile.body == friendly_unit.team or  tile.head is not None:
                return False

            return True

        x, y = friendly_unit.position

        possibleMoves = [
            world.position_to_tile_map[(x + 1, y)],
            world.position_to_tile_map[(x, y + 1)],
            world.position_to_tile_map[(x - 1, y)],
            world.position_to_tile_map[(x, y - 1)]
        ]

        viableMoves = [move for move in possibleMoves if viable(move)]

        if not viableMoves:
            next_move = choose_random_from(possibleMoves).position

        else:
            next_move = choose_random_from(viableMoves).position


        friendly_unit.move(next_move)
        print("MyAI Turn {0}: currently at {1}, making move to {2}.".format(
            str(self.turn_count),
            str(friendly_unit.position),
            next_move
        ))
