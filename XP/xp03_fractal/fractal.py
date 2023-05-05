"""Draw a fractal."""

from PIL import Image


class Fractal:
    """Beautiful fractal."""

    def __init__(self, size, scale, computation):
        """Constructor.

        Arguments:
        size -- the size of the image as a tuple (x, y)
        scale -- the scale of x and y as a list of 2-tuple
                 [(minimum_x, minimum_y), (maximum_x, maximum_y)]
                 these are mathematical coordinates
        computation -- the function used for computing pixel values as a function
        """
        self.max_value = 100
        self.size = size
        self.scale = scale
        self.computation = computation
        self.computed_data = []

    def compute(self):
        """Create the fractal by computing every pixel value."""
        for y in range(self.size[1]):
            row = []
            for x in range(self.size[0]):
                row.append(self.pixel_value((x, y)))
            # print(row)
            self.computed_data.append(row)

    def pixel_value(self, pixel):
        """
        Return the number of iterations it took for the pixel to go out of bounds.

        Arguments:
        pixel -- the pixel coordinate (x, y)

        Returns:
        the number of iterations of computation it took to go out of bounds as integer.
        """
        x = pixel[0]
        y = pixel[1]
        x_min = self.scale[0][0]
        x_max = self.scale[1][0]
        y_min = self.scale[0][1]
        y_max = self.scale[1][1]
        size_x = self.size[0]
        size_y = self.size[1]
        x = x / size_x
        x = x * (x_max - x_min)
        x = x + x_min
        y = y / size_y
        y = y * (y_max - y_min)
        y = y + y_min
        x_original = x
        y_original = y
        counter = 0
        while x ** 2 + y ** 2 <= 4 and counter < self.max_value - 1:
            counter += 1
            x, y = self.computation(x, y, x_original, y_original)
        return counter

    def value_to_rgb(self, value):
        """Value to RGB."""
        value = value / self.max_value
        colour = int(value * 256)
        return colour, colour, colour

    def save_image(self, filename):
        """
        Save the image to hard drive.

        Arguments:
        filename -- the file name to save the file to as a string.
        """
        im = Image.new("RGB", self.size)
        for y, row in enumerate(self.computed_data):
            for x, value in enumerate(row):
                im.putpixel((x, y), self.value_to_rgb(value))
        im.save(filename)
        im.show()


def mandelbrot_computation(x: float, y: float, x_original: float, y_original: float) -> tuple:
    """
    Return single iteration result of computation as tuple[x, y].

    :param x - mathematical x coordinate (transformed)
    :param y - mathematical y coordinate (transformed)
    :param x_original - mathematical x coordinate of pixel
    :param y_original - mathematical y coordinate of pixel

    :return tuple[x, y] after single iteration
    """
    z = complex(x, y)
    z_original = complex(x_original, y_original)
    z_squared = z ** 2
    complex_sum = z_squared + z_original
    x_result = complex_sum.real
    y_result = complex_sum.imag
    return x_result, y_result


def julia_computation(x: float, y: float, x_original: float, y_original: float) -> tuple:
    """
    Return single iteration result of computation as tuple[x, y].

    For different c and n make new function rather than change these constants.
    Otherwise tester will not give you any points :p

    :param x - mathematical x coordinate (transformed)
    :param y - mathematical y coordinate (transformed)
    :param x_original - mathematical x coordinate of pixel
    :param y_original - mathematical y coordinate of pixel

    :return tuple[x, y] after single iteration
    """
    c = -0.7869 + 0.1889j  # DO NOT CHANGE
    n = 3  # DO NOT CHANGE
    z = complex(x, y)
    z_squared = z ** n
    complex_sum = z_squared + c
    x_result = complex_sum.real
    y_result = complex_sum.imag
    return x_result, y_result


def ship_computation(x: float, y: float, x_original: float, y_original: float) -> tuple:
    """
    Return single iteration result of computation as tuple[x, y].

    You should invert y axis for correct results and picture

    :param x - mathematical x coordinate (transformed)
    :param y - mathematical y coordinate (transformed)
    :param x_original - mathematical x coordinate of pixel
    :param y_original - mathematical y coordinate of pixel

    :return tuple[x, y] after single iteration
    """
    z = complex(abs(x), abs(y))
    z_squared = z**2
    c = complex(x_original, -y_original)
    total = z_squared + c
    return total.real, total.imag


if __name__ == "__main__":
    """
    mandelbrot = Fractal((500, 500), [(-2.2, -1.5), (1, 1.5)], mandelbrot_computation)
    mandelbrot = Fractal((400, 400), [(-0.75, 0.105), (-0.74, 0.115)], mandelbrot_computation)
    mandelbrot = Fractal((1000, 1000), [(-0.74877, 0.065053), (-0.74872, 0.065103)], mandelbrot_computation)
    # mandelbrot.compute()
    mandelbrot.save_image("mandelbrot.png")
    julia = Fractal((500, 500), [(-2, -2), (2, 2)], julia_computation)
    julia.compute()
    julia.save_image("julia.png")
    ship = Fractal((500, 500), [(-2, -2), (2, 2)], ship_computation)
    ship = Fractal((1000, 1000), [(-1.8, -0.1), (-1.7, 0.02)], ship_computation)
    ship.compute()
    ship.save_image("ship.png")
    """
