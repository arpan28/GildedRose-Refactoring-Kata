# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseMainTest(unittest.TestCase):
    """
    Test suite for the GildedRose inventory update system
    """

    def setUp(self):
        """
        Set up the initial list of items for testing before each test method runs..
        """
        self.items = [
            Item(name="+5 Dexterity Vest", sell_in=10, quality=20),
            Item(name="Aged Brie", sell_in=2, quality=0),
            Item(name="Elixir of the Mongoose", sell_in=5, quality=7),
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=49),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49),
            Item(name="Conjured Mana Cake", sell_in=3, quality=6),
        ]
        self.gilded_rose = GildedRose(self.items)

    def _update_and_assert(self, expected_states, days=1):
        """
        Helper method to update quality for a given number of days
        and assert the expected final state of all items.

        Args:
            expected_states (list): A list of tuples (name, sell_in, quality)
                                    representing the expected state of items.
            days (int): The number of days to simulate.
        """
        for _ in range(days):
            self.gilded_rose.update_quality()


        current_states = sorted([(item.name, item.sell_in, item.quality) for item in self.items], key=lambda x: x[0])
        expected_states_sorted = sorted(expected_states, key=lambda x: x[0])

        self.assertEqual(len(current_states), len(expected_states_sorted), "Number of items changed unexpectedly.")
        for i, (current_name, current_sell_in, current_quality) in enumerate(current_states):
            expected_name, expected_sell_in, expected_quality = expected_states_sorted[i]
            with self.subTest(item_name=current_name, day_simulated=days):
                self.assertEqual(current_name, expected_name, f"Name mismatch for item at index {i}")
                self.assertEqual(current_sell_in, expected_sell_in, f"SellIn mismatch for {current_name} after {days} day(s)")
                self.assertEqual(current_quality, expected_quality, f"Quality mismatch for {current_name} after {days} day(s)")

    def test_after_1_day(self):
        """
        Test the state of all items after 1 day of updates.
        """
        expected_states_day_1 = [
            ("+5 Dexterity Vest", 9, 19),
            ("Aged Brie", 1, 1),
            ("Elixir of the Mongoose", 4, 6),
            ("Sulfuras, Hand of Ragnaros", 0, 80),
            ("Sulfuras, Hand of Ragnaros", -1, 80),
            ("Backstage passes to a TAFKAL80ETC concert", 14, 21),
            ("Backstage passes to a TAFKAL80ETC concert", 9, 50), # 49 + 2 = 51, capped at 50
            ("Backstage passes to a TAFKAL80ETC concert", 4, 50), # 49 + 3 = 52, capped at 50
            ("Conjured Mana Cake", 2, 4), # 6 - 2 = 4
        ]
        self._update_and_assert(expected_states_day_1, days=1)

    def test_after_2_days(self):
        """
        Test the state of all items after 2 days of updates.
        This corresponds to the 'days=2' in your original main function (0, 1).
        """
        # Simulate 2 days and check the final state
        expected_states_day_2 = [
            ("+5 Dexterity Vest", 8, 18),
            ("Aged Brie", 0, 2),
            ("Elixir of the Mongoose", 3, 5),
            ("Sulfuras, Hand of Ragnaros", 0, 80),
            ("Sulfuras, Hand of Ragnaros", -1, 80),
            ("Backstage passes to a TAFKAL80ETC concert", 13, 22),
            ("Backstage passes to a TAFKAL80ETC concert", 8, 50),
            ("Backstage passes to a TAFKAL80ETC concert", 3, 50),
            ("Conjured Mana Cake", 1, 2), # 4 - 2 = 2
        ]
        self._update_and_assert(expected_states_day_2, days=2)


 

    def test_conjured_item_past_sell_date_multiple_days(self):
        """
        Test Conjured item specific behavior over more days.
        """
        self.items = [
            Item(name="Conjured Mana Cake", sell_in=1, quality=6),
        ]
        self.gilded_rose = GildedRose(self.items)

        # Day 1: sell_in 0, quality 4
        self._update_and_assert([("Conjured Mana Cake", 0, 4)], days=1)

        # Day 2: sell_in -1, quality 0 (4 - 4 = 0)
        self._update_and_assert([("Conjured Mana Cake", -1, 0)], days=1)

        # Day 3: sell_in -2, quality 0 (still 0)
        self._update_and_assert([("Conjured Mana Cake", -2, 0)], days=1)


if __name__ == "__main__":
    unittest.main()
