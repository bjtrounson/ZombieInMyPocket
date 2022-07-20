import unittest
from cards.card import Card
from cards.card_manager import CardManager
from cards.time_action import TimeAction
from cards.neutral_time_behaviour import NeutralTimeBehaviour
from cards.item_time_behaviour import ItemTimeBehaviour
from cards.bad_time_behaviour import BadTimeBehaviour
from cards.good_time_behaviour import GoodTimeBehaviour
from items.item import Item
from items.item_type import ItemType


class CardTestCases(unittest.TestCase):

    def test_when_card_has_more_than_3_time_actions_expect_exception_raised(self):
        time_actions = [TimeAction(9, NeutralTimeBehaviour("You try hard not to wet yourself")),
                        TimeAction(10, ItemTimeBehaviour("ITEM", Item(ItemType.Oil))),
                        TimeAction(11, BadTimeBehaviour(6, "6 Zombies")),
                        TimeAction(11, BadTimeBehaviour(6, "6 Zombies")),
                        ]
        self.assertRaises(Exception, Card, time_actions)

    def test_when_card_has_only_3_time_actions_expect_no_exception_raised(self):
        raised = False
        try:
            time_actions = [TimeAction(9, NeutralTimeBehaviour("You try hard not to wet yourself")),
                            TimeAction(10, ItemTimeBehaviour("ITEM", Item(ItemType.Oil))),
                            TimeAction(11, BadTimeBehaviour(6, "6 Zombies")),
                            ]
            Card(time_actions)
        except None:
            raised = True
        self.assertFalse(raised, "Exception raised")

    def test_when_card_with_item_expect_has_item(self):
        time_actions = [TimeAction(9, NeutralTimeBehaviour("You try hard not to wet yourself")),
                        TimeAction(10, ItemTimeBehaviour("ITEM", Item(ItemType.Oil))),
                        TimeAction(11, BadTimeBehaviour(6, "6 Zombies")),
                        ]
        card = Card(time_actions)
        expected_time_behaviour = time_actions[1].time_behaviour.action()
        actual_time_behaviour = card.get_time_action(10).time_behaviour.action()
        self.assertEqual(expected_time_behaviour, actual_time_behaviour)

    def test_when_card_with_bad_time_behaviour_expect_number_of_damage(self):
        time_actions = [TimeAction(9, NeutralTimeBehaviour("You try hard not to wet yourself")),
                        TimeAction(10, ItemTimeBehaviour("ITEM", Item(ItemType.Oil))),
                        TimeAction(11, BadTimeBehaviour(6, "6 Zombies")),
                        ]
        card = Card(time_actions)
        expected_damage = 6
        actual_damage = card.get_time_action(11).time_behaviour.action()
        self.assertEqual(expected_damage, actual_damage)

    def test_when_card_with_neutral_time_behaviour_expect_message(self):
        time_actions = [TimeAction(9, NeutralTimeBehaviour("You try hard not to wet yourself")),
                        TimeAction(10, ItemTimeBehaviour("ITEM", Item(ItemType.Oil))),
                        TimeAction(11, BadTimeBehaviour(6, "6 Zombies")),
                        ]
        card = Card(time_actions)
        expected_message = "You try hard not to wet yourself"
        actual_message = card.get_time_action(9).time_behaviour.action()
        self.assertEqual(expected_message, actual_message)

    def test_when_card_with_good_time_behaviour_expect_number_of_health(self):
        time_actions = [TimeAction(9, NeutralTimeBehaviour("You try hard not to wet yourself")),
                        TimeAction(10, ItemTimeBehaviour("ITEM", Item(ItemType.Oil))),
                        TimeAction(11, GoodTimeBehaviour("Candybar in your pocket", 1)),
                        ]
        card = Card(time_actions)
        expected_health = 1
        actual_health = card.get_time_action(11).time_behaviour.action()
        self.assertEqual(expected_health, actual_health)

    def test_when_card_manager_add_all_cards_creates_cards(self):
        card_manager = CardManager()
        card_manager.add_all_cards()
        self.assertIsInstance(card_manager.get_deck(), list)


if __name__ == '__main__':
    unittest.main()
