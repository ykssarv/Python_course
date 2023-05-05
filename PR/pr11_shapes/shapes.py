"""Shapes."""
import math


class Shape:
    """General shape class."""

    def __init__(self, color: str):
        """Constructor, sets the color."""
        self.color = color

    def set_color(self, color: str):
        """Set the color of the shape."""
        self.color = color

    def get_color(self) -> str:
        """Get the color of the shape."""
        return self.color

    def get_area(self):
        """Get area method which every subclass has to override."""
        print("Implement area")


class Circle(Shape):
    """Circle is a subclass of Shape."""

    def __init__(self, color: str, radius: float):
        """
        Constructor of the circle.

        The color is stored using superclass constructor:
        super().__init__(color)

        The radius value is stored here.
        """
        super().__init__(color)
        self.radius = radius

    def __repr__(self) -> str:
        """
        Return representation of the circle.

        For this exercise, this should return a string:
        Circle (r: {radius}, color: {color})
        """
        return "Circle (r: " + str(self.radius) + ", color: " + str(self.color) + ")"

    def get_area(self) -> float:
        """
        Calculate the area of the circle.

        Area of the circle is pi * r * r.
        """
        return math.pi * self.radius * self.radius


class Square(Shape):
    """Square is a subclass of Shape."""

    def __init__(self, color: str, side: float):
        """
        Constructor of the square.

        The color is stored using superclass constructor:
        super().__init__(color)

        The side value is stored here.
        """
        super().__init__(color)
        self.side = side

    def __repr__(self) -> str:
        """
        Return representation of the square.

        For this exercise, this should return a string:
        Square (a: {side}, color: {color})
        """
        return "Square (a: " + str(self.side) + ", color: " + str(self.color) + ")"

    def get_area(self) -> float:
        """
        Calculate the area of the square.

        Area of the square is side * side.
        """
        return self.side * self.side


class Rectangle(Shape):
    """Rectangle is a subclass of Shape."""

    def __init__(self, color: str, length: float, width: float):
        """
        Constructor of the rectangle.

        The color is stored using superclass constructor:
        super().__init__(color)

        The side value is stored here.
        """
        super().__init__(color)
        self.length = length
        self.width = width

    def __repr__(self) -> str:
        """
        Return representation of the rectangle.

        For this exercise, this should return a string:
        """
        return f"Rectangle (l: {self.length}, w: {self.width}, color: {self.color})"

    def get_area(self) -> float:
        """
        Calculate the area of the square.

        Area of the square is length * width.
        """
        return self.length * self.width


class Paint:
    """The main program to manipulate the shapes."""

    def __init__(self):
        """Constructor should create a list to store all the shapes."""
        self.all_shapes = []

    def add_shape(self, shape: Shape) -> None:
        """Add a shape to the program."""
        self.all_shapes.append(shape)

    def get_shapes(self) -> list:
        """Return all the shapes."""
        return self.all_shapes

    def calculate_total_area(self) -> float:
        """Calculate total area of the shapes."""
        total_area = 0
        for shape in self.all_shapes:
            total_area += shape.get_area()
        return total_area

    def get_circles(self) -> list:
        """Return only circles."""
        circles = []
        for shape in self.all_shapes:
            if isinstance(shape, Circle):
                circles.append(shape)
        return circles

    def get_squares(self) -> list:
        """Return only squares."""
        squares = []
        for shape in self.all_shapes:
            if isinstance(shape, Square):
                squares.append(shape)
        return squares

    def get_rectangles(self) -> list:
        """Return only rectangles."""
        rectangles = []
        for shape in self.all_shapes:
            if isinstance(shape, Rectangle):
                rectangles.append(shape)
        return rectangles


if __name__ == '__main__':
    paint = Paint()
    circle = Circle("blue", 10)
    square = Square("red", 11)
    paint.add_shape(circle)
    paint.add_shape(square)
    print(paint.calculate_total_area())
    print(paint.get_circles())
