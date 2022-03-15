from tiles.door_positions import DoorPosition


class Door:
    door_position: DoorPosition

    def __init__(self, door_position: DoorPosition):
        self.door_position = door_position
