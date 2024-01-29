"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    near_earth_objects = []
    with open(neo_csv_path, newline="") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            row["name"] = row["name"] if row["name"] else None
            row["diameter"] = (
                float(row["diameter"]) if row["diameter"] else float("nan")
            )
            row["pha"] = False if row["pha"] in ["", "N"] else True
            try:
                neo = NearEarthObject(
                    designation=row["pdes"],
                    name=row["name"],
                    diameter=row["diameter"],
                    hazardous=row["pha"],
                )
            except Exception as e:
                print(e)
            else:
                near_earth_objects.append(neo)

    return near_earth_objects


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    close_approachs = []

    with open(cad_json_path, newline="") as json_file:
        json_reader = json.load(json_file)
        data = json_reader["data"]
        default_fields = [
            "des",
            "orbit_id",
            "jd",
            "cd",
            "dist",
            "dist_min",
            "dist_max",
            "v_rel",
            "v_inf",
            "t_sigma_f",
            "h",
        ]
        fields = json_reader.get("fields", default_fields)
        for row in data:
            try:
                row = dict(zip(fields, row))
                approach = CloseApproach(
                    designation=row["des"],
                    time=row["cd"],
                    distance=float(row["dist"]),
                    velocity=float(row["v_rel"]),
                )
            except Exception as e:
                print(e)
            else:
                close_approachs.append(approach)

    return close_approachs
