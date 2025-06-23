# -*- coding: utf-8 -*-

class GildedRose(object):
    """
    Manages the inventory of items at the Gilded Rose inn, updating their
    sell_in and quality values daily according to specific rules for different
    item types.
    """

    def __init__(self, items):
        """
        Initializes the GildedRose system with a list of Item objects.

        Args:
            items (list): A list of Item objects representing the inventory.
        """
        self.items = items
        # Define a dictionary to map specific item names to their update strategies.
        self._update_strategies = {
            "Aged Brie": self._update_aged_brie,
            "Backstage passes to a TAFKAL80ETC concert": self._update_backstage_pass,
            # Normal items and Conjured items are handled outside this dictionary
            # due to their more general or substring-based matching rules.
        }

    def _update_item_quality_bounds(self, item):
        """
        Ensures an item's quality stays within the allowed bounds (0 to 50).
        "Sulfuras" is an exception and its quality is not bound.
        This method should be called after all other quality adjustments for the day.
        """
        # "Sulfuras" has a fixed quality of 80 and is not subject to the 0-50 bounds.
        if item.name == "Sulfuras, Hand of Ragnaros":
            return 

        if item.quality > 50:
            item.quality = 50
        if item.quality < 0:
            item.quality = 0

    def _update_normal_item(self, item):
        """
        Updates quality and sell_in for a normal item.
        Quality degrades by 1 per day, and twice as fast after sell_in date passes.
        """
        # Decrease quality
        item.quality -= 1

        # Decrease sell_in
        item.sell_in -= 1

        # If sell_in date has passed, quality degrades an additional time
        if item.sell_in < 0:
            item.quality -= 1

    def _update_aged_brie(self, item):
        """
        Updates quality and sell_in for "Aged Brie".
        Quality increases by 1 per day, and twice as fast after sell_in date passes.
        """
        # Increase quality
        item.quality += 1

        # Decrease sell_in
        item.sell_in -= 1

        # If sell_in date has passed, quality increases an additional time
        if item.sell_in < 0:
            item.quality += 1

    def _update_backstage_pass(self, item):
        """
        Updates quality and sell_in for "Backstage passes".
        Quality increases based on sell_in remaining days, drops to 0 after concert.
        """
        # Increase quality normally
        item.quality += 1

        # Additional quality increase if sell_in is 10 days or less
        if item.sell_in < 11:
            item.quality += 1 # Increase by 1 (total +2)
        # Additional quality increase if sell_in is 5 days or less
        if item.sell_in < 6:
            item.quality += 1 # Increase by 1 (total +3)

        # Decrease sell_in
        item.sell_in -= 1

        # If sell_in date has passed (concert over), quality drops to 0
        if item.sell_in < 0:
            item.quality = 0

    def _update_conjured_item(self, item):
        """
        Updates quality and sell_in for "Conjured" items.
        Quality degrades twice as fast as normal items (by 2 per day, by 4 after sell_in).
        """
        # Decrease quality by 2 (twice as fast as normal)
        item.quality -= 2

        # Decrease sell_in
        item.sell_in -= 1

        # If sell_in date has passed, quality degrades an additional 2 times (total -4)
        if item.sell_in < 0:
            item.quality -= 2

    def update_quality(self):
        """
        Orchestrates the daily update of quality and sell_in for all items.
        Delegates specific item update logic to private helper methods using a strategy map.
        """
        for item in self.items:
            # "Sulfuras" is a legendary item; its quality and sell_in never change.
            if item.name == "Sulfuras, Hand of Ragnaros":
                continue # Skip all updates for Sulfuras
            if "Conjured" in item.name:
                self._update_conjured_item(item)
            else:
                updater_func = self._update_strategies.get(item.name, self._update_normal_item)
                updater_func(item)

            # Ensure quality is within bounds (0 to 50) for all items except Sulfuras
            self._update_item_quality_bounds(item)


class Item:
    """
    Represents an item in the Gilded Rose inventory.
    Do not alter this class as per the requirements specification.
    """
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        """
        Returns a string representation of the Item object.
        """
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

