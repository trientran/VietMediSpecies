import pandas as pd
import requests
import time

# Load your CSV file
df = pd.read_csv("scientificName_updated.csv")

# Prepare a list to hold API results
results = []

# Function to query GBIF API
def query_gbif(name):
    url = "https://api.gbif.org/v1/species/match"
    params = {"name": name}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "inputName": name,
            "usageKey": data.get("usageKey"),
            "scientificName": data.get("scientificName"),
            "canonicalName": data.get("canonicalName"),
            "rank": data.get("rank"),
            "status": data.get("status"),
            "confidence": data.get("confidence"),
            "matchType": data.get("matchType"),
            "kingdom": data.get("kingdom"),
            "phylum": data.get("phylum"),
            "class": data.get("class"),
            "order": data.get("order"),
            "family": data.get("family"),
            "genus": data.get("genus"),
            "species": data.get("species"),
            "kingdomKey": data.get("kingdomKey"),
            "phylumKey": data.get("phylumKey"),
            "classKey": data.get("classKey"),
            "orderKey": data.get("orderKey"),
            "familyKey": data.get("familyKey"),
            "genusKey": data.get("genusKey"),
            "speciesKey": data.get("speciesKey"),
            "synonym": data.get("synonym")
        }
    except Exception as e:
        return {"inputName": name, "error": str(e)}

# Loop through species and query the API
for name in df["scientificName"]:
    result = query_gbif(name)
    results.append(result)
    # time.sleep(0.5)  # Be kind to the API

# Save results to a new CSV
output_df = pd.DataFrame(results)
output_df.to_csv("gbif_species_match_results_4.csv", index=False)
print("Results saved to gbif_species_match_results_4.csv")
