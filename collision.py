from objects.enemy import Enemy
from objects.bonus import Bonus
from objects.finish import Finish
from objects.tile import Tile


def get_collisions(target_entity, objects, is_player):
    collisions = []
    for obj in objects:
        if target_entity.colliderect(obj.rect) and (is_player or type(obj) != Bonus):
            collisions.append(obj)
    return collisions


def get_first_collision(collisions, axis, direction):
    if axis == "x":
        if direction == "left":
            max_index = 0
            for index in range(1, len(collisions)):
                if collisions[max_index].rect.x < collisions[index].rect.x:
                    max_index = index
            return max_index
        elif direction == "right":
            min_index = 0
            for index in range(1, len(collisions)):
                if collisions[min_index].rect.x > collisions[index].rect.x:
                    min_index = index
            return min_index
    elif axis == "y":
        if direction == "up":
            max_index = 0
            for index in range(1, len(collisions)):
                if collisions[max_index].rect.y < collisions[index].rect.y:
                    max_index = index
            return max_index
        elif direction == "down":
            min_index = 0
            for index in range(1, len(collisions)):
                if collisions[min_index].rect.y > collisions[index].rect.y:
                    min_index = index
            return min_index


def move_and_collide(target_entity, move_params, objects, is_player):
    up_collision = False
    down_collision = False
    left_collision = False
    right_collision = False

    collide_enemy = []
    collide_bonus = []
    killed_enemies = []
    is_finish = False

    check_move_params = [1, 1]

    # Facem mai intai miscarea pe axa X
    target_entity.x += move_params[0]
    # Preluam coliziunile de pe axa X
    collisions = get_collisions(target_entity, objects, is_player)

    if len(collisions) > 0:
        object_index = 0
        # Coliziune in stanga
        if move_params[0] < 0:
            # Cautam obiectul del mai din dreapta cu care a intrat in coliziune
            max_index = get_first_collision(collisions, "x", "left")
            # Punem target_entity exact in dreapta acelui obiect
            target_entity.x = collisions[max_index].rect.x + collisions[max_index].rect.width

            left_collision = True
            check_move_params[0] = 0
            object_index = max_index

        # Coliziune in dreapta
        elif move_params[0] > 0:
            # Cautam obiectul del mai din stanga cu care a intrat in coliziune
            min_index = get_first_collision(collisions, "x", "right")
            # Punem target_entity exact in stanga acelui obiect
            target_entity.x = collisions[min_index].rect.x - target_entity.width

            right_collision = True
            check_move_params[0] = 0
            object_index = min_index

        if type(collisions[object_index]) == Enemy:
            collide_enemy += [collisions[object_index]]
        elif type(collisions[object_index]) == Bonus:
            collide_bonus += [collisions[object_index]]
        elif type(collisions[object_index]) == Finish:
            is_finish = True
        elif type(collisions[object_index]) != Tile:
            collide_bonus += [collisions[object_index]]

    # Apoi facem miscarea pe axa Y
    target_entity.y += move_params[1]
    # Preluam coliziunile de pe axa Y
    collisions = get_collisions(target_entity, objects, is_player)

    if len(collisions) > 0:
        object_index = 0
        # Coliziune in sus
        if move_params[1] < 0:
            # Cautam obiectul del mai de jos cu care a intrat in coliziune
            max_index = get_first_collision(collisions, "y", "up")
            # Punem target_entity exact sub acel obiect
            target_entity.y = collisions[max_index].rect.y + collisions[max_index].rect.height

            up_collision = True
            check_move_params[1] = 0
            object_index = max_index

        elif move_params[1] > 0:
            # Cautam obiectul del mai de sus cu care a intrat in coliziune
            min_index = get_first_collision(collisions, "y", "down")
            # Punem target_entity exact deasupra acelui obiect
            target_entity.y = collisions[min_index].rect.y - target_entity.height

            down_collision = True
            check_move_params[1] = 0
            object_index = min_index

            if type(collisions[object_index]) == Enemy:
                down_collision = False
                killed_enemies += [collisions[object_index]]

        if type(collisions[object_index]) == Enemy:
            collide_enemy += [collisions[object_index]]
        elif type(collisions[object_index]) == Bonus:
            collide_bonus += [collisions[object_index]]
        elif type(collisions[object_index]) == Finish:
            is_finish = True
        elif type(collisions[object_index]) != Tile:
            collide_bonus += [collisions[object_index]]

    return {"up": up_collision, "down": down_collision, "left": left_collision,
            "right": right_collision}, check_move_params, collide_enemy, collide_bonus, killed_enemies, is_finish


# for obj in collisions:
#     # Coliziune in sus
#     if move_params[1] < 0:
#         target_entity.y = obj.y + obj.height
#         up_collision = True
#         check_move_params[1] = 0
#
#     # Coliziune in jos
#     elif move_params[1] > 0:
#         target_entity.y = obj.y - target_entity.height
#         down_collision = True
#         check_move_params[1] = 0


# for obj in collisions:
#     # Coliziune in stanga
#     if move_params[0] < 0:
#         target_entity.x = obj.x + obj.width
#         left_collision = True
#         check_move_params[0] = 0
#
#     # Coliziune in dreapta
#     elif move_params[0] > 0:
#         target_entity.x = obj.x - target_entity.width
#         right_collision = True
#         check_move_params[0] = 0
