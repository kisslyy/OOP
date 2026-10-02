import math


class Point2D:
    total_points_count = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        Point2D.total_points_count += 1

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f})"

    def __repr__(self):
        return f"Point2D(x={self.x:.2f}, y={self.y:.2f})"

    def distance_to(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    @classmethod
    def origin(cls):
        return cls(0.0, 0.0)

    @classmethod
    def clone(cls, point):
        return cls(point.x, point.y)

    @classmethod
    def from_polar(cls, r, theta_degrees):
        theta = math.radians(theta_degrees)
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        return cls(x, y)

    @staticmethod
    def distance_between(p1, p2):
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


point1 = Point2D(1.234, 6.789)
point2 = Point2D(4.0, 2.0)

print(str(point1))
print(repr(point1))

print(point1.distance_to(point2))

point3 = Point2D.origin()
print(point3)

point4 = Point2D.clone(point1)
print(point4)
print(point4 is point1)

point5 = Point2D.from_polar(5.0, 60.0)
print(point5)

print(Point2D.distance_between((0.0, 0.0), (3.0, 4.0)))

print(Point2D.total_points_count)