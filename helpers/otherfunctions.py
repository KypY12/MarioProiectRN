def draw_objects(objects, scroll_movement):
    for object in objects:
        object.draw(scroll_movement)


# def draw_tiles(rects, scroll_move):
#     for rect in rects:
#         rect.draw(scroll_move)
#         # if type(rect) != Player:
#             # rect.x -= scroll_move[0]
#             # rect.y -= scroll_move[1]
#             # (player_coords[0] + scroll_move[0] - PLAYER_BACK_OFFSET)/20
#             # rect.y -= (player_coords[1] + scroll_move[1])/20
#             # pygame.draw.rect(window, (255, 255, 255), rect, 0)

#
# def move_and_draw_enemies(enemies, rects, scroll_move):
#     for enemy in enemies:
#         enemy.move(rects)
#         enemy.draw(scroll_move)
