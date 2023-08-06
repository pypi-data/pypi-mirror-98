from wurst.geo import geomatcher
from . import DATA_DIR

REGION_MAPPING_FILEPATH = DATA_DIR / "regionmappingH12.csv"


class Geomap:
    """
    Map ecoinvent locations to IAM regions and vice-versa.
    """

    def __init__(self):

        self.geo = self.get_IAM_geomatcher()

    @staticmethod
    def get_IAM_geomatcher():
        """
        Geographical boundaries for IMAGE regions are initally included in geomatcher.
        However, they are not properly labelled.

        """

        d_image_regions = {
            "BRA": "Brazil",
            "CAN": "Canada",
            "CEU": "Central Europe",
            "CHN": "China Region",
            "EAF": "Eastern Africa",
            "INDIA": "India",
            "INDO": "Indonesia Region",
            "JAP": "Japan",
            "KOR": "Korea Region",
            "ME": "Middle east",
            "MEX": "Mexico",
            "NAF": "Northern Africa",
            "OCE": "Oceania",
            "RCAM": "Central America",
            "RSAF": "Rest of Southern Africa",
            "RSAM": "Rest of South America",
            "RSAS": "Rest of South Asia",
            "RUS": "Russia Region",
            "SAF": "South Africa",
            "SEAS": "South Asia",
            "STAN": "Central Asia",
            "TUR": "Turkey",
            "UKR": "Ukraine region",
            "USA": "USA",
            "WAF": "Western Africa",
            "WEU": "Western Europe",
        }

        d_map = {("IMAGE", v): ("IMAGE", k) for k, v in d_image_regions.items()}

        new_def = dict()

        for k, v in geomatcher.items():
            if isinstance(k, tuple):
                if k[0] == "IMAGE" and k[1] in list(d_image_regions.values()):
                    new_def[d_map[k]] = v

        geo = geomatcher

        for k in list(geomatcher.keys()):
            if k[0] == "IMAGE" and k[1] in list(d_image_regions.values()):
                geomatcher.pop(k)

        geo.update(new_def)

        with open(REGION_MAPPING_FILEPATH) as f:
            f.readline()
            csv_list = [[val.strip() for val in r.split(";")] for r in f.readlines()]
            l = [(x[1], x[2]) for x in csv_list]

        # List of countries not found
        countries_not_found = ["CC", "CX", "GG", "JE", "BL"]

        rmnd_to_iso = {}
        iso_to_rmnd = {}

        # Build a dictionary that maps region names (used by REMIND) to ISO country codes
        # And a reverse dictionary that maps ISO country codes to region names
        for ISO, region in l:
            if ISO not in countries_not_found:
                try:
                    rmnd_to_iso[region].append(ISO)
                except KeyError:
                    rmnd_to_iso[region] = [ISO]

                iso_to_rmnd[region] = ISO

        geo.add_definitions(rmnd_to_iso, "REMIND")

        return geo


    def iam_to_ecoinvent_location(self, location, contained=False):
        """
        Find the corresponding ecoinvent region given an IAM region.

        :param location: name of a IAM region
        :type location: str
        :return: name of an ecoinvent region
        :rtype: str
        """

        if location == "World":
            return ["GLO"]

        ecoinvent_locations = []



        searchfunc = self.geo.contained if contained else self.geo.intersects

        for iam in ("REMIND", "IMAGE"):
            loc = (iam, location)

            try:
                searchfunc(loc)
                for r in searchfunc(loc):
                    if not isinstance(r, tuple):
                        ecoinvent_locations.append(r)

            except KeyError:
                pass

        if len(ecoinvent_locations) == 0:
            print("Can't find location {} using the geomatcher.".format(location))

        return ecoinvent_locations

    def ecoinvent_to_iam_location(self, location):
        """
        Return an IAM region name for a 2-digit ISO country code given.
        Set rules in case two IAM regions are within the ecoinvent region.

        :param location: 2-digit ISO country code
        :type location: str
        :return: IAM region name
        :rtype: str
        """

        mapping = {
            "GLO": "World",
            "RoW": "CAZ" if self.model == "remind" else "World",
        }
        if location in mapping:
            return mapping[location]

        iam_location = [
            r[1]
            for r in self.geo.within(location)
            if r[0] == self.model.upper() and r[1] != "World"
        ]

        mapping = {
            ("AFR", "MEA"): "AFR",
            ("AFR", "SSA"): "AFR",
            ("EUR", "NEU"): "EUR",
            ("EUR", "REF"): "EUR",
            ("OAS", "CHA"): "OAS",
            ("OAS", "EUR"): "OAS",
            ("OAS", "IND"): "OAS",
            ("OAS", "JPN"): "OAS",
            ("OAS", "MEA"): "OAS",
            ("OAS", "REF"): "OAS",
            ("USA", "CAZ"): "USA",
        }

        # If we have more than one REMIND region
        if len(iam_location) > 1:
            # TODO: find a more elegant way to do that
            for key, value in mapping.items():
                # We need to find the most specific REMIND region
                if len(set(iam_location).intersection(set(key))) == 2:
                    iam_location.remove(value)
            return iam_location[0]
        elif len(iam_location) == 0:

            # There are a few ecoinvent regions that do not match well
            # with IMAGE regions

            if self.model == "image":

                d_ecoinvent_regions = {
                    "ENTSO-E": "WEU",
                    "RER": "WEU",
                    "RNA": "USA",
                    "RAS": "SEAS",
                    "RAF": "RSAF",
                    "Europe without Switzerland": "WEU",
                    "RLA": "RSAF",
                    "XK": "WEU",
                    "SS": "EAF",
                    "IAI Area, Africa": "WAF",
                    "UN-OCEANIA": "OCE",
                    "UCTE": "CEU",
                    "CU": "RCAM",
                    "IAI Area, Asia, without China and GCC": "RSAS",
                    "IAI Area, South America": "RSAM",
                    "IAI Area, EU27 & EFTA": "WEU",
                    "IAI Area, Russia & RER w/o EU27 & EFTA": "RUS"
                }

            if self.model == "remind":
                d_ecoinvent_regions = {
                    "IAI Area, Russia & RER w/o EU27 & EFTA": "REF",
                }

            if location in d_ecoinvent_regions:
                return d_ecoinvent_regions[location]
            else:
                print("no location for {}".format(location))

            # It can also be that the location is already
            # an IAM location

            list_IAM_regions = [
                k
                for k in list(self.geo.geo.keys())
                if isinstance(k, tuple) and k[0].lower() == self.model.lower()
            ]

            if location in list_IAM_regions:
                return location

            print("no location for {}".format(location))
        else:
            return iam_location[0]

    def iam_to_GAINS_region(self, location):
        """
        Regions defined in GAINS emission data follows REMIND naming convention, but is different from IMAGE.
        :param location:
        :return:
        """

        d_map_region = {
            "BRA": "LAM",
            "CAN": "CAZ",
            "CEU": "EUR",
            "CHN": "CHA",
            "EAF": "SSA",
            "INDIA": "IND",
            "INDO": "OAS",
            "JAP": "JPN",
            "KOR": "OAS",
            "ME": "MEA",
            "MEX": "LAM",
            "NAF": "SSA",
            "OCE": "CAZ",
            "RCAM": "LAM",
            "RSAF": "SSA",
            "RSAM": "LAM",
            "RSAS": "OAS",
            "RUS": "REF",
            "SAF": "SSA",
            "SEAS": "OAS",
            "STAN": "MEA",
            "TUR": "MEA",
            "UKR": "REF",
            "USA": "USA",
            "WAF": "SSA",
            "WEU": "EUR",
            "World": "EUR",
        }

        if self.model == "remind":
            return location

        if self.model == "image":
            return d_map_region[location]
