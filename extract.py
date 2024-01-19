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
import sys
from collections.abc import Collection

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    near_earth_objects = set()
    # TODO: Load NEO data from the given CSV file.
    with open(neo_csv_path, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            near_earth_objects.add(NearEarthObject(row))

    return near_earth_objects

def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    close_approachs = set()
    # TODO: Load close approach data from the given JSON file.
    with open(cad_json_path, newline='') as json_file:
        json_reader = json.load(json_file)
        data = json_reader['data']
        default_fields = [
            "des", "orbit_id", "jd", "cd", "dist", "dist_min", "dist_max", "v_rel", "v_inf", "t_sigma_f", "h"
        ]
        fields = json_reader.get('fields', default_fields)
        for row in data:
            row = dict(zip(fields, row))
            close_approachs.add( CloseApproach(row))

    return close_approachs

if __name__ == '__main__':
    # neo_csv_path = "./tests/test-neos-2020.csv"
    # neos = load_neos(neo_csv_path)

    cad_json_path = "./data/cad.json"
    cads = load_approaches(cad_json_path)

