import sys
import os
import PIL.ImageDraw as ImageDraw,PIL.Image as Image, PIL.ImageShow as ImageShow 


class Point(object):
    def __init__(self, x, y):
        self.X = x
        self.Y = y
    def __getitem__(self, item):
        return self.X if item == "X" else self.Y
    def distance(self, point):
        return abs(self.X - point.X) + abs(self.Y - point.Y)

def up(point, distance):
    return Point(point.X, point.Y + distance)
def down(point, distance):
    return Point(point.X, point.Y - distance)
def left(point, distance):
    return Point(point.X - distance, point.Y)
def right(point, distance):
    return Point(point.X + distance, point.Y)

new_point_getter = {
    "U": up,
    "D": down,
    "L": left,
    "R": right
}

def intersect2(p1, p2, q1, q2):
    a1 = p2.Y - p1.Y
    b1 = p1.X - p2.X
    c1 = a1 * p1.X + b1 * p1.Y

    a2 = q2.Y - q1.Y
    b2 = q1.X - q2.X
    c2 = a2 * q1.X + b2 * q1.Y

    determinant = a1 * b2 - a2 * b1

    if (determinant == 0):
        return Point(0,0)
    else:
        x = (b2 * c1 - b1 * c2) / determinant
        y = (a1 * c2 - a2 * c1) / determinant

        if (x >= min(p1.X, p2.X) and x <= max(p1.X, p2.X) and y >= min(p1.Y, p2.Y) and y <= max(p1.Y, p2.Y) and
            x >= min(q1.X, q2.X) and x <= max(q1.X, q2.X) and y >= min(q1.Y, q2.Y) and y <= max(q1.Y, q2.Y)):
            return Point(x, y)
        else:
            return Point(0,0)

def get_points(directions):
    last_point = Point(0, 0)
    points = []
    for direction in directions:
        last_point = new_point_getter.get(direction[0])(last_point, int(direction[1:]))
        points.append(last_point)
    return points

def get_closest_cross(fwp, swp):
    origin = Point(0,0)
    closest_distance_cross = sys.maxsize
    closest_intersection_point = Point(0,0)
    last_fwp = fwp[0]    
    for first_wire_point in fwp[1:]:
        last_swp = swp[0]
        for second_wire_point in swp[1:]:
            intersection = intersect2(first_wire_point, last_fwp, second_wire_point, last_swp)
            if intersection.X > 0 or intersection.Y > 0:
                distance = intersection.distance(origin)
                if distance < closest_distance_cross:
                    closest_distance_cross = distance
                    closest_intersection_point = intersection
            last_swp = second_wire_point
        last_fwp = first_wire_point
    return closest_intersection_point


data = []
with open(os.path.dirname(os.path.realpath(__file__)) + '\input.txt', 'r') as file:
    data = file.read().splitlines()

first_wire_directions = data[0].split(",")
second_wire_directions = data[1].split(",")

first_wire_points = get_points(first_wire_directions)
second_wire_points = get_points(second_wire_directions)

im = Image.new("RGB", (600,600))
draw = ImageDraw.Draw(im)

offset = 200
last_fwd_point = Point(0,0)
for point in first_wire_points:
    draw.line((last_fwd_point.X + offset, last_fwd_point.Y + offset, point.X + offset, point.Y + offset), fill=(0, 0, 255))
    last_fwd_point = point

last_fwd_point = Point(0,0)
for point in second_wire_points:
    draw.line((last_fwd_point.X + offset, last_fwd_point.Y + offset, point.X + offset, point.Y + offset), fill=(0, 255, 0))
    last_fwd_point = point

closest_intersection_point = get_closest_cross(first_wire_points, second_wire_points)
draw.point((closest_intersection_point.X + offset, closest_intersection_point.Y + offset), fill=255)
print('Distance from port to closest intersection point is {0}'.format(closest_intersection_point.distance(Point(0,0))))

im.show()
