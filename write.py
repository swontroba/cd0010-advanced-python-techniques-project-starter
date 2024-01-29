"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    cols = (
        "datetime_utc",
        "distance_au",
        "velocity_km_s",
        "designation",
        "name",
        "diameter_km",
        "potentially_hazardous",
    )
    with open(filename, "w", newline="") as write_out:
        writer = csv.DictWriter(write_out, fieldnames=cols)
        writer.writeheader()
        for result in results:
            row = {**result.serialize(), **result.neo.serialize()}
            row["name"] = row["name"] if row["name"] is not None else ""
            row["potentially_hazardous"] = (
                "True" if row["potentially_hazardous"] else "False"
            )
            writer.writerow(row)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    json_data = []
    for result in results:
        row = {**result.serialize(), **result.neo.serialize()}
        row["name"] = row["name"] if row["name"] is not None else ""
        row["potentially_hazardous"] = (
            bool(1) if row["potentially_hazardous"] else bool(0)
        )
        json_data.append(
            {
                "datetime_utc": row["datetime_utc"],
                "distance_au": row["distance_au"],
                "velocity_km_s": row["velocity_km_s"],
                "neo": {
                    "designation": row["designation"],
                    "name": row["name"],
                    "diameter_km": row["diameter_km"],
                    "potentially_hazardous": row["potentially_hazardous"],
                },
            }
        )

    with open(filename, "w") as write_out:
        json.dump(json_data, write_out, indent="\t")
