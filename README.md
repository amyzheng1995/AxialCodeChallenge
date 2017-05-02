# AxialCodeChallenge

## Problem Statement:
Using the data structure in the attached sample_data.json, develop a match engine.  For each seller, find the matching buyers.  A match means the seller and buyer have at least one intersecting industry and at least one intersecting geography.  Come up with a simple rule to rank the matching buyers to a seller.

## Commands:
```
python3 match_engine.py --seller_id 1640fb77-135c-43d4-8196-835e07245683
python3 match_engine.py --all
```

## Run tests:
```
python3 -m unittest test_match_engine.py
```

## Assumptions:
- sample_data.json file is correctly formatted with double quotes
- For --all command, if the seller doesn't have a match, it will not be displayed
- If a buyer matches the seller with industry ID, 2 points will be given. If it is matched with geography ID, 1 point will be given
- The result will be output to a different file. If it is searched by seller ID, a json file named seller ID will be created. If it is searched by --all, all_sellers json file will be created
- The ranking will be displayed in descending order based on the points
