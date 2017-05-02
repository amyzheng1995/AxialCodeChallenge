import json
import argparse
import collections


class Entity:
    def __init__(self, id, geo_ids, ind_ids, ent_type):
        self.id = id
        self.geography_ids = geo_ids
        self.industry_ids = ind_ids
        self.ent_type = ent_type


def parse_data(data_file):
    try:
        with open(data_file, "r") as input_file:
            data = json.load(input_file)
    except ValueError:
        raise
    except IOError:
        raise

    # Save the buyers and sellers in separate dictionaries
    # The key would be the buyer/seller ID and value would be class Entity
    buyers = {}
    sellers = {}
    for entity in data:
        try:
            entity_details = entity["details"]
            new_ent = Entity(entity["id"], [str(x) for x in entity_details["geography_ids"]],
                             [str(x) for x in entity_details["industry_ids"]], entity["type"])
            if entity.get("type") == "buyer":
                buyers[entity["id"]] = new_ent
            elif entity.get("type") == "seller":
                sellers[entity["id"]] = new_ent
            else:
                print("{0} is not a valid entity type!".format(entity.get("type")))
                continue
        except KeyError as key_err:
            print("Missing key in data: {0}".format(repr(key_err)))
            continue

    return buyers, sellers


def map_details(buyers):
    details_dict = {
        "geography_ids": {},
        "industry_ids": {}
    }
    # Find the unique geography_ids and industry_ids in buyers dictionary and
    # add the the buyers ID to the unique industry/geography ID
    for key, b in buyers.items():
        geo_ids = b.geography_ids
        ind_ids = b.industry_ids
        for g in geo_ids:
            if str(g) not in details_dict["geography_ids"]:
                details_dict["geography_ids"][str(g)] = []
            details_dict["geography_ids"][str(g)].append(b.id)

        for i in ind_ids:
            if str(i) not in details_dict["industry_ids"]:
                details_dict["industry_ids"][str(i)] = []
            details_dict["industry_ids"][str(i)].append(b.id)
    return details_dict


def map_result_count(buyers_geo, buyers_ind):
    # Create a dictionary of buyer and counter
    geo_count = collections.Counter(buyers_geo)
    ind_count = collections.Counter(buyers_ind)
    # Find the buyers with intersections in both geography and industry
    intersections = list(set(buyers_geo) & set(buyers_ind))
    if len(intersections) > 0:
        point_map = {}

        # For every industry match, weight is 2
        # For every geography match, weight is 1
        for each in intersections:
            point = 0
            point += geo_count[each]
            point += ind_count[each] * 2
            point_map[each] = point
        sorted_keys = sorted(point_map, key=point_map.get, reverse=True)
        # Sort the rank in descending order
        result = {}
        for r in sorted_keys:
            result[r] = point_map[r]
        return result
    else:
        print("no match")
        return


def find_buyer(buyer_mapping, seller_details):
    geography_list = list(buyer_mapping.get("geography_ids").keys())
    industry_list = list(buyer_mapping.get("industry_ids").keys())
    seller_geo_list = seller_details.geography_ids
    seller_ind_list = seller_details.industry_ids

    # Intersect to find common geography and industry
    geo_intersect = list(set(seller_geo_list) & set(geography_list))
    ind_intersect = list(set(seller_ind_list) & set(industry_list))

    # If there is intersections in both, proceed with mapping
    if len(geo_intersect) > 0 and len(ind_intersect) > 0:
        buyers_geo = []
        buyers_ind = []
        for g in geo_intersect:
            buyers_geo.extend(buyer_mapping["geography_ids"][g])

        for i in ind_intersect:
            buyers_ind.extend(buyer_mapping["industry_ids"][i])

        return map_result_count(buyers_geo, buyers_ind)
    else:
        print("There is nothing in common for geography and industry")
        return


def find_all_buyers(buyer_mapping, sellers):
    result_list = {}
    # Loop through sellers dictionary and call find_buyer method
    for id, seller in sellers.items():
        buyers = find_buyer(buyer_mapping, seller)
        if buyers is not None:
            result_list[id] = buyers

    return result_list


def main(args):
    buyers = {}
    sellers = {}

    try:
        buyers, sellers = parse_data(args.data_file)
    except ValueError:
        print("Invalid json given as input file!")
    except IOError as io_err:
        print("Could not open given input file {0}".format(io_err))

    buyer_mapping = map_details(buyers)

    if args.seller_id:
        if args.seller_id in sellers:
            with open("{0}.json".format(args.seller_id), "w") as out_file:
                out_file.write(json.dumps(find_buyer(buyer_mapping, sellers[args.seller_id]), indent=2))
        else:
            print("There is no such seller")
    else:
        with open("all_sellers.json", "w") as out_file:
            out_file.write(json.dumps(find_all_buyers(buyer_mapping, sellers), indent=2))


if __name__ == "__main__":
    # Parse arguments given in command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_file", default="sample_data.json")
    parser.add_argument("--seller_id", help="The ID of a seller")
    parser.add_argument("--all", action="store_true", default=False)
    args = parser.parse_args()

    main(args)
