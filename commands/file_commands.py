from commands.command import Command


class FileCommands(Command):
    def __init__(self, cwd):
        super().__init__(cwd)

    def do_save_game_options(self, file_name: str) -> None:
        self._file_manager.serialize_game_options_to_json(file_name, self._game_options)

    def do_load_game_options(self, file_name: str) -> None:
        try:
            game_options = self._file_manager.deserialize_json_to_game_options(file_name)
            self._game.get_player_from_level().set_health(game_options.player_health)
            self._game.get_player_from_level().set_attack_score(game_options.player_damage)
            self._game.get_player_from_level().set_item_limit(game_options.player_item_limit)
            self._game.set_game_start_time(game_options.game_start_time)
            self._game.set_game_end_time(game_options.game_end_time)
        except Exception as e:
            print(e)

    def do_save_game(self, file_name: str) -> None:
        self._pickle_manager.serialize_object_to_file(file_name, self._game)

    def do_load_game(self, file_name: str) -> None:
        self._game = self._pickle_manager.deserialize_file_to_object(file_name)