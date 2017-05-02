import unittest
from match_engine import Entity
from match_engine import map_details
from match_engine import find_all_buyers
from match_engine import find_buyer


class TestStringMethods(unittest.TestCase):

    def test_Entity(self):
        entity = Entity("1234", [22, 12], [23,21], "seller")
        self.assertEqual(entity.id, "1234")
        self.assertEqual(entity.ent_type, "seller")
        self.assertEqual(entity.geography_ids, [22, 12])
        self.assertEqual(entity.industry_ids, [23, 21])

    def test_map_details(self):
        buyer_entity1 = Entity("b123", [22, 12], [23, 21], "buyer")
        buyer_entity2 = Entity("b234", [11, 12], [13, 14], "buyer")

        buyers = {
            "b123": buyer_entity1,
            "b234": buyer_entity2
        }
        result = map_details(buyers)
        expected_result = {
            "geography_ids": {"22": ["b123"], "11": ["b234"], "12": ["b123", "b234"]},
            "industry_ids": {"23": ["b123"], "21": ["b123"], "13": ["b234"], "14": ["b234"]}
        }
        self.assertEqual(result, expected_result)

    def test_find_buyer(self):
        buyer_mapping = {
            "geography_ids": {"22": ["b123"], "11": ["b234"], "12": ["b123", "b234"]},
            "industry_ids": {"23": ["b123"], "21": ["b123"], "13": ["b234"], "14": ["b234"]}
        }
        seller_entity = Entity("s123", ["22", "12"], ["23", "21"], "seller")
        result = find_buyer(buyer_mapping, seller_entity)
        self.assertEqual(result, {"b123": 6})

    def test_find_all_buyers(self):
        buyer_mapping = {
            "geography_ids": {"22": ["b123"], "11": ["b234"], "12": ["b123", "b234"]},
            "industry_ids": {"23": ["b123"], "21": ["b123"], "13": ["b234"], "14": ["b234"]}
        }
        seller_entity1 = Entity("s123", ["22", "12"], ["23", "21"], "seller")
        seller_entity2 = Entity("s234", ["2", "10"], ["4", "8"], "seller")

        sellers = {
            "s123": seller_entity1,
            "s234": seller_entity2
        }
        self.assertEqual(find_all_buyers(buyer_mapping, sellers), {'s123': {'b123': 6}})


if __name__ == "__main__":
    unittest.main()