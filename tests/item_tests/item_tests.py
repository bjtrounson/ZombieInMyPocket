import unittest
from items.item import Item
from items.item_type import ItemType


class ItemTestCases(unittest.TestCase):
    def test_when_item_with_negative_behaviour_expect_damage(self):
        item = Item(ItemType.BoardWNail)
        expected_damage = 1
        actual_damage = item.action()
        self.assertEqual(expected_damage, actual_damage)

    def test_when_item_with_positive_behaviour_expect_health(self):
        item = Item(ItemType.CanOfSoda)
        expected_health = 2
        actual_health = item.action()
        self.assertEqual(expected_health, actual_health)

    def test_when_item_with_limited_uses_expect_uses_to_go_down(self):
        item = Item(ItemType.Chainsaw)
        item.action()
        expected_uses = 1
        actual_uses = item.uses
        self.assertEqual(expected_uses, actual_uses)


if __name__ == '__main__':
    unittest.main()
