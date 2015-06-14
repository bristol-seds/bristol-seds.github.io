# Generates simplifies outlines for countries_world.json
import json

# Define functions for translating to/from grids
import mpl_toolkits.basemap.pyproj as pyproj # Import the pyproj module

wgs84=pyproj.Proj(proj='merc', ellps='WGS84') # LatLon with WGS84 datum

# lon/lat to x/y grid
def lonlat_to_ea_grid(outlines):
    return [[wgs84(point[0], point[1]) for point in outline] for outline in outlines]

# x/y grid to lon/lat
def ea_grid_to_lonlat(outlines):
    return [[wgs84(point[0], point[1], inverse=True) for point in outline] for outline in outlines]

#
# from http://mappinghacks.com/code/dp.py.txt
#

# pure-Python Douglas-Peucker line simplification/generalization
#
# this code was written by Schuyler Erle <schuyler@nocat.net> and is
#   made available in the public domain.
#
# the code was ported from a freely-licensed example at
#   http://www.3dsoftware.com/Cartography/Programming/PolyLineReduction/
#
# the original page is no longer available, but is mirrored at
#   http://www.mappinghacks.com/code/PolyLineReduction/

"""

>>> line = [(0,0),(1,0),(2,0),(2,1),(2,2),(1,2),(0,2),(0,1),(0,0)]
>>> simplify_points(line, 1.0)
[(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)]

>>> line = [(0,0),(0.5,0.5),(1,0),(1.25,-0.25),(1.5,.5)]
>>> simplify_points(line, 0.25)
[(0, 0), (0.5, 0.5), (1.25, -0.25), (1.5, 0.5)]

"""

import math

def simplify_points (pts, tolerance):
    anchor  = 0
    floater = len(pts) - 1
    stack   = []
    keep    = set()

    stack.append((anchor, floater))
    while stack:
        anchor, floater = stack.pop()

        # initialize line segment
        if pts[floater] != pts[anchor]:
            anchorX = float(pts[floater][0] - pts[anchor][0])
            anchorY = float(pts[floater][1] - pts[anchor][1])
            seg_len = math.sqrt(anchorX ** 2 + anchorY ** 2)
            # get the unit vector
            anchorX /= seg_len
            anchorY /= seg_len
        else:
            anchorX = anchorY = seg_len = 0.0

        # inner loop:
        max_dist = 0.0
        farthest = anchor + 1
        for i in range(anchor + 1, floater):
            dist_to_seg = 0.0
            # compare to anchor
            vecX = float(pts[i][0] - pts[anchor][0])
            vecY = float(pts[i][1] - pts[anchor][1])
            seg_len = math.sqrt( vecX ** 2 + vecY ** 2 )
            # dot product:
            proj = vecX * anchorX + vecY * anchorY
            if proj < 0.0:
                dist_to_seg = seg_len
            else:
                # compare to floater
                vecX = float(pts[i][0] - pts[floater][0])
                vecY = float(pts[i][1] - pts[floater][1])
                seg_len = math.sqrt( vecX ** 2 + vecY ** 2 )
                # dot product:
                proj = vecX * (-anchorX) + vecY * (-anchorY)
                if proj < 0.0:
                    dist_to_seg = seg_len
                else:  # calculate perpendicular distance to line (pythagorean theorem):
                    dist_to_seg = math.sqrt(abs(seg_len ** 2 - proj ** 2))
                if max_dist < dist_to_seg:
                    max_dist = dist_to_seg
                    farthest = i

        if max_dist <= tolerance: # use line segment
            keep.add(anchor)
            keep.add(floater)
        else:
            stack.append((anchor, farthest))
            stack.append((farthest, floater))

    keep = list(keep)
    keep.sort()
    return [pts[i] for i in keep]


def prepare_simple_grids(grids, tolerance=2*2000): # Approx 2km
    simple = [simplify_points(points, tolerance) for points in grids]
    return [s for s in simple if len(s) > 2]


# We'll need a utility function for splitting outlines that cross the antiprime meridian
def fix_antiprime_outlines(outlines):
    new_outlines = []

    for outline in outlines:

        east = False
        west = False
        for point in outline:
            if point[0] > 150: east = True
            if point[0] < -150: west = True

        if east and west: # This outline crosses the antiprime. Presume it doesn't cross the -30th meridian
            east_outline = []
            west_outline = []

            for point in outline: # Split the outline
                lon = point[0]
                east_outline.append((lon if lon > -30 else  180, point[1]))
                west_outline.append((lon if lon < -30 else -180, point[1]))

            east_outline_strip = []
            west_outline_strip = []

            for i in range(len(east_outline)): # Strip runs of points that lie on the meridian
                if not (east_outline[i-1][0] == 180 and east_outline[i][0] == 180 and east_outline[(i+1)%len(east_outline)][0] == 180):
                    east_outline_strip.append(east_outline[i])

            for i in range(len(west_outline)):
                if not(west_outline[i-1][0] == -180 and west_outline[i][0] == -180 and west_outline[(i+1)%len(west_outline)][0] == -180):
                    west_outline_strip.append(west_outline[i])

            #print "Remove", len(outline)
            #print "East", len(east_outline_strip)
            #print "West", len(west_outline_strip)

            # Swap in these outlines
            new_outlines.append(east_outline_strip)
            new_outlines.append(west_outline_strip)
        else:
            new_outlines.append(outline)

    return new_outlines


# Load country outlines
with open('countries_world.json') as data_file:
    countries = json.load(data_file)

# Now convert all countries to grids
for c in countries:
    c['grids'] = lonlat_to_ea_grid(c['outlines'])
    c['simple_grids'] = prepare_simple_grids(c['grids'])
    c['simple_outlines'] = fix_antiprime_outlines(ea_grid_to_lonlat(c['simple_grids']))

# Write out again
outfile = open('countries_world.json','w')
print >>outfile, json.dumps(countries, sort_keys=True, indent=2)

outfile.close()
