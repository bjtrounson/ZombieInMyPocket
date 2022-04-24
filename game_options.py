from dataclasses import dataclass


@dataclass
class GameOptions:
    player_health: int
    player_damage: int
    player_item_limit: int
    game_start_time: int
    game_end_time: int

