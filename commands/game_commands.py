from commands.command import Command


class GameCommands(Command):
    def __init__(self, cwd):
        super().__init__(cwd)

    def do_game_info(self, args) -> None:
        print(f"Current Tile: {self._game.get_current_tile().tile_name}")
        print(f"Player Health: {self._game.get_player_from_level().get_health()}")
        print(f"Player Attack: {self._game.get_player_from_level().get_attack_score()}")
        print(f"Player Items: {[item.item_name for item in self._game.get_player_from_level().get_items()]}")
        print(f"Player Position X: {self._game.get_player_from_level().get_x()} "
              f"Y: {self._game.get_player_from_level().get_y()}")

    def do_next_turn(self, args) -> None:
        next_tile = self._game.draw_tile()
        current_tile = self._game.get_current_tile()
        entry_door = None
        while entry_door is None:
            try:
                entry_door = self._game.get_door_from_input(next_tile, True)
            except ValueError as e:
                print(e)
        exit_door = None
        while exit_door is None:
            try:
                exit_door = self._game.get_door_from_input(current_tile, False)
            except ValueError as e:
                print(e)
        self._game.move(entry_door, exit_door, next_tile)
        self._game.draw_dev_card()
        self._game.activate_time_action(self._game.get_current_dev_card())

        if self._game.get_player_from_level().get_health() <= 0:
            print("Game Over! You Died")

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def do_cower(self, args) -> None:
        self._game.cower()
