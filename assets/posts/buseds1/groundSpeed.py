#!/usr/bin/python
import math


def angle_between(vec1, vec2):
    dot_product = dot_product_spherical(vec1, vec2)

    vec1mag = math.sqrt(dot_product_spherical(vec1, vec1))
    vec2mag = math.sqrt(dot_product_spherical(vec2, vec2))

    alpha = math.acos(dot_product / (vec1mag * vec2mag))
    return alpha

def dot_product_spherical(vec1, vec2):
    abcosalpha = ((vec1[2]*vec2[2]*math.cos(vec1[0])*math.cos(vec2[0])*math.cos(vec1[1])*math.cos(vec2[1]))
               + (vec1[2]*vec2[2]*math.cos(vec1[0])*math.cos(vec2[0])*math.sin(vec1[1])*math.sin(vec2[1]))
               + (vec1[2]*vec2[2]*math.sin(vec1[0])*math.sin(vec2[0])))

    return abcosalpha

# Finds the ground distance between two spherical vectors
# Works well only for vectors with a small angular difference
def ground_distance_covered(vec1, vec2):
    distance = math.sqrt(2) * vec1[2] * math.sqrt(1 - math.cos(angle_between(vec1, vec2)))

    return distance

start = [math.radians(52.08505),math.radians(-2.13590),6400]
end = [math.radians(51.09622),math.radians(-2.72175),6400]
x = ground_distance_covered(start, end)
print(x)
