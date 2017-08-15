"""
Author: austinscchiang
Description: Given raw parsed data, parse the file for a placing-to-fantasy-
points key-value pair. Collect all key-value pairs and stream the complete
placing-to-points conversion into an output file.
"""
from __future__ import print_function


INPUT_FILE = "data.txt"
OUTPUT_FILE = "placing_rewards.txt"

def placings_read(input_file=INPUT_FILE):
    place_to_points = {}
    with open(input_file, "rb") as f:
        for line in f:
            tokens = line.split()
            if (len(tokens) == 2 and
                tokens[0].isdigit() and
                tokens[1].isdigit()):
                place = int(tokens[0])
                points = int(tokens[1])
                if (place in place_to_points and
                    not place_to_points[place] == points):
                    raise ValueError("""Place does not always correspond to same
                                     point value""")

                place_to_points[place] = points

    return place_to_points

def placings_write(mapping, output_file=OUTPUT_FILE):
    with open (output_file, "wb") as w:
        for key in sorted(mapping):
            print("{} {}".format(key, mapping[key]), file=w)


if __name__ == "__main__":
    place_to_points = placings_read()
    placings_write(place_to_points)
