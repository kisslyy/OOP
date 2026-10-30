import math


class Point3d:
    _total_points_count = 0

    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        Point3d._total_points_count += 1

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    def __repr__(self):
        return f"Point3d(x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f})"

    def distance_to(self, other):
        return math.sqrt(
            (other.x - self.x) ** 2 +
            (other.y - self.y) ** 2 +
            (other.z - self.z) ** 2
        )

    @classmethod
    def origin(cls):
        return cls(0.0, 0.0, 0.0)

    @classmethod
    def clone(cls, point):
        return cls(point.x, point.y, point.z)

    @classmethod
    def from_polar(cls, r, theta_degrees, phi_degrees):
        theta = math.radians(theta_degrees)
        phi = math.radians(phi_degrees)

        x = r * math.cos(phi) * math.cos(theta)
        y = r * math.cos(phi) * math.sin(theta)
        z = r * math.sin(phi)

        return cls(x, y, z)

    @staticmethod
    def distance_between(p1, p2):
        return math.sqrt(
            (p2[0] - p1[0]) ** 2 +
            (p2[1] - p1[1]) ** 2 +
            (p2[2] - p1[2]) ** 2
        )


class Vector3d:
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    def __repr__(self):
        return f"Vector3d(x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f})"

    @classmethod
    def from_points(cls, start, end):
        return cls(
            end.x - start.x,
            end.y - start.y,
            end.z - start.z
        )

    @staticmethod
    def _get_components(other):
        if isinstance(other, Vector3d):
            return other.x, other.y, other.z

        if isinstance(other, (int, float)):
            return other, other, other

        return None

    def _length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __eq__(self, other):
        if not isinstance(other, Vector3d):
            return NotImplemented

        return (
            self.x == other.x and
            self.y == other.y and
            self.z == other.z
        )

    def __gt__(self, other):
        if not isinstance(other, Vector3d):
            return NotImplemented

        return self._length() > other._length()

    def __lt__(self, other):
        if not isinstance(other, Vector3d):
            return NotImplemented

        return self._length() < other._length()

    def __add__(self, other):
        values = self._get_components(other)

        if values is None:
            return NotImplemented

        return Vector3d(
            self.x + values[0],
            self.y + values[1],
            self.z + values[2]
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        values = self._get_components(other)

        if values is None:
            return NotImplemented

        return Vector3d(
            self.x - values[0],
            self.y - values[1],
            self.z - values[2]
        )

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return Vector3d(
                other - self.x,
                other - self.y,
                other - self.z
            )

        return NotImplemented

    def __mul__(self, other):
        values = self._get_components(other)

        if values is None:
            return NotImplemented

        return Vector3d(
            self.x * values[0],
            self.y * values[1],
            self.z * values[2]
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        values = self._get_components(other)

        if values is None:
            return NotImplemented

        return Vector3d(
            self.x / values[0],
            self.y / values[1],
            self.z / values[2]
        )

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector3d(
                other / self.x,
                other / self.y,
                other / self.z
            )

        return NotImplemented

    def __iadd__(self, other):
        values = self._get_components(other)

        if values is None:
            return NotImplemented

        self.x += values[0]
        self.y += values[1]
        self.z += values[2]

        return self

    def __isub__(self, other):
        values = self._get_components(other)

        if values is None:
            return NotImplemented

        self.x -= values[0]
        self.y -= values[1]
        self.z -= values[2]

        return self

    def __imul__(self, other):
        values = self._get_components(other)

        if values is None:
            return NotImplemented

        self.x *= values[0]
        self.y *= values[1]
        self.z *= values[2]

        return self

    def __itruediv__(self, other):
        values = self._get_components(other)

        if values is None:
            return NotImplemented

        self.x /= values[0]
        self.y /= values[1]
        self.z /= values[2]

        return self

    def __matmul__(self, other):
        if not isinstance(other, Vector3d):
            return NotImplemented

        return Vector3d(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def __len__(self):
        return int(self._length())

    def __getitem__(self, key):
        if isinstance(key, str):
            if key in ("x", "y", "z"):
                return getattr(self, key)

            raise KeyError(key)

        return (self.x, self.y, self.z)[key]

    def __iter__(self):
        return iter((self.x, self.y, self.z))


point1 = Point3d(4.23334, 17.73489, 5.22345)
point2 = Point3d(54, 223.999, 15)

print(str(point1))
print(repr(point1))

print(point1.distance_to(point2))

point3 = Point3d.origin()
print(point3)

point4 = Point3d.clone(point1)
print(point4)
print(point4 is point1)

point5 = Point3d.from_polar(5.0, 60.0, 30.0)
print(point5)

print(Point3d.distance_between((0, 0, 0), (3, 4, 12)))

print(Point3d._total_points_count)


vector1 = Vector3d(3, 4, 5)
vector2 = Vector3d(1, 2, 3)

vector3 = Vector3d.from_points(point1, point2)
print(vector3)

print(vector1 == vector2)
print(vector1 > vector2)
print(vector1 < vector2)

print(vector1 + vector2)
print(vector1 - vector2)
print(vector1 * vector2)
print(vector1 / vector2)

print(vector1 + 3)
print(3 + vector1)

print(vector1 - 3)
print(3 - vector1)

print(vector1 * 3)
print(3 * vector1)

print(vector1 / 3)
print(30 / vector1)


vector4 = Vector3d(6, 8, 10)
vector4_id = id(vector4)

vector4 += Vector3d(1, 2, 3)
print(vector4, id(vector4) == vector4_id)

vector4 -= 1
print(vector4, id(vector4) == vector4_id)

vector4 *= Vector3d(2, 2, 2)
print(vector4, id(vector4) == vector4_id)

vector4 /= 2
print(vector4, id(vector4) == vector4_id)


vector5 = Vector3d(1, 2, 3)
vector6 = Vector3d(4, 5, 6)

print(vector5 @ vector6)


vector7 = Vector3d(3, 4, 0)
print(len(vector7))


vector8 = Vector3d(1, 2, 3)
vector9 = Vector3d(2, 4, 6)

print((vector8 @ vector9) == Vector3d(0, 0, 0))


vector10 = Vector3d(1, 0, 0)
vector11 = Vector3d(0, 1, 0)
vector12 = Vector3d(1, 1, 0)

cross_product = vector10 @ vector11

print(
    cross_product.x * vector12.x +
    cross_product.y * vector12.y +
    cross_product.z * vector12.z == 0
)


print(vector1[0])
print(vector1["x"])

for component in vector1:
    print(component)