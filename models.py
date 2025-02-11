"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = info.get("designation", "")
        self.name = info.get("name", None)
        self.diameter = info.get("diameter", float("nan"))
        try:
            self.diameter = float(self.diameter)
        except ValueError:
            self.diameter = float("nan")
        self.hazardous = info.get("hazardous", False)

        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f"{self.name} {self.designation}"

    def __is_hazardous(self):
        """ "Returns if this NEO is hazardous in str form"""
        if self.hazardous:
            return "is"
        else:
            return "is not"

    def __str__(self):
        """Return `str(self)`."""
        return f"A NearEarthObject NEO {self.fullname} has a diameter of {self.diameter:.3f} km and {self.__is_hazardous()} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
            f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"
        )

    def serialize(self):
        """Return a dict representation of self attributes of current instance.

        Returns:
            [dict]: Keys associated with self attributes.

        """
        return {
            "designation": self.designation,
            "name": self.name,
            "diameter_km": self.diameter,
            "potentially_hazardous": self.hazardous,
        }


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.
        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = info.get("designation", "")
        self.time = cd_to_datetime(info.get("time", None))
        self.distance = float(info.get("distance", 0.0))
        self.velocity = float(info.get("velocity", 0.0))

        # Create an attribute for the referenced NEO, originally None.
        self.neo = info.get("neo", None)

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.
        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.
        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        if self.time:
            return datetime_to_str(self.time)
        return "an unknown time"

    def __str__(self):
        """Return `str(self)`."""
        return (
            f"On {self.time_str}, '{self._designation}'"
            f"approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."
        )

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
            f"velocity={self.velocity:.2f}, neo={self.neo!r})"
        )

    def serialize(self):
        """Return a dict representation of self attributes of current instance.

        Returns:
            [dict]: Keys associated with self attributes.

        """
        return {
            "datetime_utc": datetime_to_str(self.time),
            "distance_au": self.distance,
            "velocity_km_s": self.velocity,
        }


if __name__ == "__main__":
    neo_test = {
        "designation": "2020 FK",
        "name": "One REALLY BIG fake asteroid",
        "diameter": 12.34523423,
        "hazardous": True,
    }
    neo_test2 = {"designation": "2020 FK", "hazardous": True}
    neo = NearEarthObject(**neo_test2)
    print(neo.designation)
    print(neo.name)
    print(neo.diameter)
    print(neo.hazardous)
    print(neo)

    caproch_test = {
        "designation": "2020 FK",
        "time": "2099-Dec-31 20:51",
        "distance": 12.34523423,
        "velocity": 12.88,
    }
    ca = CloseApproach(**caproch_test)  # Use any sample data here.
    print(type(ca.time))
    print(ca.time_str)
    print(ca.distance)
    print(ca.velocity)
    print(ca)
