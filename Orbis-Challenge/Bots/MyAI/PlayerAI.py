from PythonClientAPI.game.PointUtils import *
from PythonClientAPI.game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.game.Enums import Team
from PythonClientAPI.game.World import World
from PythonClientAPI.game.TileUtils import TileUtils
from random import choice as choose_random_from
from math import inf

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

        closest_enemy_tile = None
        closest_enemy_distance = inf
        for point in friendly_unit.snake:
            tile = world.util.get_closest_enemy_head_from(point, [])
            distance = world.path.get_shortest_path_distance(point, tile.position)

            if distance < closest_enemy_distance:
                closest_enemy_tile = tile
                closest_enemy_distance = distance


        closest_territory_tile = world.util.get_closest_friendly_territory_from(friendly_unit.position, friendly_unit.snake)
        closest_territory_path = world.path.get_shortest_path(friendly_unit.position, closest_territory_tile.position, friendly_unit.snake)

        print("Closest Enemy Distance:  ", closest_enemy_distance)
        print("Closest Territory Distance:  ", len(closest_territory_path))

        if closest_enemy_distance < len(closest_territory_path)+1:
            self.retreat = True
            self.target = closest_territory_tile
            next_move = closest_territory_path[0]

        else:
            self.retreat = False
            self.target = None

            def viable(tile):
                if tile.is_wall or tile.body == friendly_unit.team or tile.head is not None:
                    return False

                return True

            x, y = friendly_unit.position

            possibleMoves = [
                world.position_to_tile_map[(x + 1, y)],
                world.position_to_tile_map[(x, y + 1)],
                world.position_to_tile_map[(x - 1, y)],
                world.position_to_tile_map[(x, y - 1)]
            ]

            next_move = None
            farther_point_distance = -inf

            for move in possibleMoves:
                if viable(move):
                    distance = world.path.get_shortest_path_distance(move.position, closest_territory_tile.position)

                    if distance > farther_point_distance:
                        farther_point_distance = distance
                        next_move = move.position


            if next_move is None:
                next_move = choose_random_from(possibleMoves).position


        # print("Closest_enemy_head:  ", closest_enemy_distance)
        #
        #
        # viableMoves = [move for move in possibleMoves if viable(move)]
        #
        # if not viableMoves:
        #     next_move = choose_random_from(possibleMoves).position
        #
        # else:
        #     next_move = choose_random_from(viableMoves).position


        # # if unit reaches the target point, reverse outbound boolean and set target back to None
        # if self.target is not None and friendly_unit.position == self.target.position:
        #     self.outbound = not self.outbound
        #     self.target = None
        #
        # # if outbound and no target set, set target as the closest capturable tile at least 1 tile away from your territory's edge.
        # if self.outbound and self.target is None:
        #     edges = [tile for tile in world.util.get_friendly_territory_edges()]
        #     avoid = []
        #     for edge in edges:
        #         avoid += [pos for pos in world.get_neighbours(edge.position).values()]
        #     self.target = world.util.get_closest_capturable_territory_from(friendly_unit.position, avoid)
        #
        # # else if inbound and no target set, set target as the closest friendly tile
        # elif not self.outbound and self.target is None:
        #     self.target = world.util.get_closest_friendly_territory_from(friendly_unit.position, None)
        #
        # # set next move as the next point in the path to target
        # next_move = world.path.get_shortest_path(friendly_unit.position, self.target.position, friendly_unit.snake)[0]

        # move!
        friendly_unit.move(next_move)
        print("MyAI Turn {0}: currently at {1}, {2} to {3}.".format(
            str(self.turn_count),
            str(friendly_unit.position),
            "retreating" if self.retreat else "making move",
            next_move
        ))
