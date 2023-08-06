from unittest.mock import patch

from whimsylib import bag
from whimsylib.globals import G
from whimsylib import item

from tests import common


class _Chapstick(item.Item):
    @classmethod
    def create(cls):
        return cls("chapstick")


class _BurtsBees(item.Item):
    @classmethod
    def create(cls):
        return cls("chapstick", "burt's bees")


class _ChickenWing(item.Item):
    @classmethod
    def create(cls):
        return cls("chicken wing")


class BagTest(common.EngineTest):
    def test_add_aliases_adds_holder(self):
        backpack = bag.Bag()
        pamphlet = item.Item("sycophantic propaganda pamphlet")
        backpack.add(pamphlet)
        self.assertIs(backpack, pamphlet.holder)

    @patch("whimsylib.actor.say.insayne")
    def test_add_aliases_message_for_player(self, mock_say):
        pamphlet = item.Item("sycophantic propaganda pamphlet")
        G.player.inventory.add(pamphlet)
        mock_say.assert_called_once_with(f"You acquire {pamphlet.name}.")

    @patch("whimsylib.actor.say.insayne")
    def test_add_aliases_no_message_for_npc(self, mock_say):
        backpack = bag.Bag()
        pamphlet = item.Item("sycophantic propaganda pamphlet")
        backpack.add(pamphlet)
        mock_say.assert_not_called()

    def test_items_by_name(self):
        sequined_clutch = bag.Bag()
        for _ in range(3):
            sequined_clutch.add(_ChickenWing.create())
        sequined_clutch.add(_Chapstick.create())
        sequined_clutch.add(_BurtsBees.create())
        actual = sequined_clutch.items_by_name()
        expected = {
            "chapstick": [("chapstick",), ("chapstick", "burt's bees")],
            "chicken wing": [
                ("chicken wing",),
                ("chicken wing",),
                ("chicken wing",),
            ],
        }

        # Converts items to alias tuples; otherwise, list comparison is hard
        # because Items hash by identity.
        for key, value in actual.items():
            actual[key] = sorted(item.aliases for item in value)

        self.assertEqual(expected, actual)

    def test_find(self):
        """We can find items in a bag by name, case insensitively."""
        woven_basket = bag.Bag()
        cw = _ChickenWing.create()
        cs = _Chapstick.create()
        book = item.Item("technological slavery")
        woven_basket.add(cw)
        woven_basket.add(cs)
        woven_basket.add(book)

        assert woven_basket.find("chicken wing") is cw
        assert woven_basket.find("chapstick") is cs
        assert woven_basket.find("CHAPSTICK") is cs
        assert woven_basket.find("technological slavery") is book
        assert woven_basket.find("taxidermy raccoon") is None


class BagDiscardAliasesTest(common.EngineTest):
    def setUp(self):
        self._pamphlet = item.Item("sycophantic propaganda pamphlet")
        G.player.inventory.add(self._pamphlet)

    def test_discard_aliases_removes_holder(self):
        G.player.inventory.remove(self._pamphlet)
        self.assertIsNone(self._pamphlet.holder)

    @patch("whimsylib.actor.say.insayne")
    def test_discard_aliases_message_for_player(self, mock_say):
        G.player.inventory.remove(self._pamphlet)
        mock_say.assert_called_once_with(
            f"You lose possession of {self._pamphlet.name}."
        )

    def test_discard_aliases_no_message_for_npc(self):
        backpack = bag.Bag()
        backpack.add(self._pamphlet)
        self.assertIsNot(backpack, G.player.inventory)

        with patch("whimsylib.actor.say.insayne") as mock_say:
            backpack.remove(self._pamphlet)
            mock_say.assert_not_called()
