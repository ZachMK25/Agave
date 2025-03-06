import json
import tldextract

with open("temp-links-db.json", "r") as db:
    db_contents = json.load(db)

with open("dataset.json", "r") as ds:
    ds_contents = json.load(ds)

with open("ad-tlds.json", "r") as tld:
    tlds = json.load(tld)

options = {"1": "social media", "2": "personal", "3": "resource", "4": "ad"}
results = ds_contents
changed = False
for link in db_contents["all-links"]:
    if not link in ds_contents:
        tld = tldextract.extract(link).domain
        if tld in tlds:
            results.setdefault(link, tlds[tld])
        else:
            print("LINK:", link)
            selected = input(f"enter one of: {options}")
            if selected == "q":
                break
            while (selected not in ["1", "2", "3", "4"]):
                selected = input(f"enter one of: {options}")
            print("you selected", link, "is", options[selected])
            results.setdefault(link, options[selected])
            tlds.setdefault(tld, options[selected])
            changed = True

if changed:
    with open("dataset.json", "w") as ds:
        json.dump(results, ds)
    with open("ad-tlds.json", "w") as ds:
        json.dump(tlds, ds)