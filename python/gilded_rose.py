# -*- coding: utf-8 -*-

class GildedRose(object):
    """
    Manages the inventory of items at the Gilded Rose inn, updating their
    sell_in and quality values daily according to specific rules for different
    item types.
    """

    def __init__(self, items):
        """
        Initializes the GildedRose system with a list of items.

        Args:
            items (list): A list of Item objects representing the inventory.
        """
        self.items = items

    def _update_item_quality_bounds(self, item):
        """
        Ensures an item's quality stays within the allowed bounds (0 to 50).
        Sulfuras is an exception and its quality is not bound.
        """
        # Sulfuras has a fixed quality of 80 and is not subject to the 0-50 bounds.
        if item.name != "Sulfuras, Hand of Ragnaros":
            if item.quality > 50:
                item.quality = 50
            if item.quality < 0:
                item.quality = 0

    def update_quality(self):
        """
        Updates the quality and sell_in for all items in the inventory for one day.
        This method applies specific rules for different item categories:
        - Normal items: Quality degrades by 1 per day, and twice as fast after sell_in.
        - Aged Brie: Quality increases by 1 per day, and twice as fast after sell_in.
        - Sulfuras: A legendary item; its quality and sell_in never change.
        - Backstage passes: Quality increases based on sell_in remaining days (1, 2, or 3),
                           and drops to 0 after the concert.
        - Conjured items: Quality degrades twice as fast as normal items (by 2 per day,
                          and by 4 per day after sell_in).
        """
        for item in self.items:
            # Rule: "Sulfuras", being a legendary item, never has to be sold or decreases in Quality
            if item.name == "Sulfuras, Hand of Ragnaros":
                continue # Skip all updates for Sulfuras

            # Rule: "Aged Brie" actually increases in Quality the older it gets
            if item.name == "Aged Brie":
                item.quality += 1
            # Rule: "Backstage passes" increase in Quality as its SellIn value approaches
            elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                # Quality increases by 1 normally
                item.quality += 1
                # Quality increases by 2 when there are 10 days or less
                if item.sell_in < 11:
                    item.quality += 1
                # Quality increases by 3 when there are 5 days or less
                if item.sell_in < 6:
                    item.quality += 1
            # New Rule: "Conjured" items degrade in Quality twice as fast as normal items
            # This means a base degradation of -2 per day.
            elif "Conjured" in item.name:
                item.quality -= 2
            # Default for all other "Normal" items
            else:
                item.quality -= 1

            item.sell_in -= 1


            if item.sell_in < 0:
                # Rule: Once the sell by date has passed, Quality degrades twice as fast (for normal items)
                # Rule: "Aged Brie" increases in Quality even faster once sell_in passes
                if item.name == "Aged Brie":
                    item.quality += 1
                # Rule: "Backstage passes" Quality drops to 0 after the concert
                elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                    item.quality = 0
                # New Rule: "Conjured" items degrade twice as fast (additional degradation after sell_in)
                # This makes the total degradation -4 per day after sell_in.
                elif "Conjured" in item.name:
                    item.quality -= 2
                # Default for all other "Normal" items: degrade an additional time.
                # This makes the total degradation -2 per day after sell_in.
                else:
                    item.quality -= 1

            # Rule: The Quality of an item is never negative
            # Rule: The Quality of an item is never more than 50
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

