"""Shapes."""

class Shape:
    """General shape class."""

    def __init__(self, color: str):
        """Constructor, sets the color."""
        pass

    def set_color(self, color: str):
        """Set the color of the shape."""
        pass

    def get_color(self) -> str:
        """Get the color of the shape."""
        pass

    def get_area(self) -> float:
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
        pass

    def __repr__(self) -> str:
        """
        Return representation of the circle.

        For this exercise, this should return a string:
        Circle (r: {radius}, color: {color})
        """
        pass

    def get_area(self) -> float:
        """
        Calculate the area of the circle.

        Area of the circle is pi * r * r.
        """
        pass


class Square(Shape):
    """Square is a subclass of Shape."""

    def __init__(self, color: str, side: float):
        """
        Constructor of the square.

        The color is stored using superclass constructor:
        super().__init__(color)

        The side value is stored here.
        """
        pass

    def __repr__(self) -> str:
        """
        Return representation of the square.

        For this exercise, this should return a string:
        Square (a: {side}, color: {color})
        """
        pass

    def get_area(self) -> float:
        """
        Calculate the area of the square.

        Area of the square is side * side.
        """
        pass


# class Rectangle(Shape):


class Paint:
    """The main program to manipulate the shapes."""

    def __init__(self):
        """Constructor should create a list to store all the shapes."""
        pass

    def add_shape(self, shape: Shape) -> None:
        """Add a shape to the program."""
        pass

    def get_shapes(self) -> list:
        """
        Return all the shapes.
        """
        pass

    def calculate_total_area(self) -> float:
        """
        Calculate total area of the shapes.
        """
        pass

    def get_circles(self) -> list:
        """Return only circles."""
        pass

    def get_squares(self) -> list:
        """Return only squares."""
        pass

    def get_rectangles(self) -> list:
        """Return only rectangles."""
        pass


if __name__ == '__main__':
    paint = Paint()
    circle = Circle("blue", 10)
    square = Square("red", 11)
    paint.add_shape(circle)
    paint.add_shape(square)
    print(paint.calculate_total_area())
    print(paint.get_circles())
