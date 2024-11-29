import math
import os
import numpy as np
from PIL import Image
import random

NUMBER_OF_PIXELS = 28 * 28
IMAGE_SIZE = 28


def get_chars(filename):
    """
    Reads the classes of characters
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))

    try:
        with open(os.path.join(dir_path, '..', filename)) as file:
            chars = [line[0] for line in file]

        return chars

    except FileNotFoundError:
        print("File %s was not found." % filename)
        raise
    except Exception as e:
        print("Something terrible happened: %s", str(e))
        raise


def get_images(filename):
    """
    Reads the images (black pixel is 1, white pixel is 0 in the input)
    Trasnforms (0, 1) values to (-1.0, 1.0)
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    vectors = []

    try:
        with open(os.path.join(dir_path, '..', filename)) as file:
            for line in file:
                vectors.append([1.0 if float(v) == 1 else -1.0 for v in line.strip().split(',')])

        return vectors

    except FileNotFoundError:
        print("File %s was not found." % filename)
        raise
    except Exception as e:
        print("Something terrible happened: %s", str(e))
        raise


class Perceptron:
    """ Perceptron
        :attr data: list of objects that represent images
    """

    def __init__(self, images, chars):
        idata = get_images(images)
        cdata = get_chars(chars)

        self.weights = [0 for _ in range(NUMBER_OF_PIXELS)]
        self.data = [{'vector': v, 'char': c} for (v, c) in zip(idata, cdata)]
        random.seed()

    def errors_exist(self, weights, target_char, opposite_char, data):
        for idx, image in enumerate(data):
            z = 0
            image_pixels = image["vector"]
            image_char = image["char"]

            for idx, pixel in enumerate(image_pixels):
                z += pixel * weights[idx]

            # print(z, image_char, target_char, opposite_char)

            if z >= 0 and image_char == opposite_char:
                # print(z, image_char, opposite_char)
                return True
            if z < 0 and image_char == target_char:
                # print(z, image_char, target_char)
                return True

        return False




    def train(self, target_char, opposite_char, steps):
        weights = [0 for _ in range(NUMBER_OF_PIXELS)]
        learning_rate = 1

        data = [e for e in self.data if e['char'] in (target_char, opposite_char)]

        i = 0
        while self.errors_exist(weights, target_char, opposite_char, data) and steps > 0:
            print(i, i/len(data)*100, end="\r")
            z = 0

            if i >= len(data): 
                print(weights)
                print("Loops left", steps)
                steps -= 1
                i = 0

            image = data[i]["vector"]
            image_char = data[i]["char"]

            for idx, pixel in enumerate(image):
                z += int(pixel) * weights[idx]

            if z >= 0 and image_char == opposite_char:
                for idx in range(NUMBER_OF_PIXELS):
                    # weights[idx] -= image[idx] * learning_rate
                    weights[idx] -= image[idx]
            if z < 0 and image_char == target_char:
                for idx in range(NUMBER_OF_PIXELS):
                    # weights[idx] += image[idx] * learning_rate
                    weights[idx] += image[idx]

            i += 1

        self.weights = weights
        

    def test(self, target_char, opposite_char):
        """Tests the learned perceptron with the last 1000 x,y pairs.
        (Note that this only counts those ones that belong either to the plus or minus classes.)

        :param target_char: the target character we are trying to distinguish
        :param opposite_char: the opposite character
        :return: the ratio of correctly classified characters
        """
        success = 0
        examples = self.data[5000:]

        examples = [e for e in examples if e['char'] in (target_char, opposite_char)]

        for e in examples:
            z = np.dot(e['vector'], self.weights)
            if (z >= 0 and e['char'] == target_char) or (z < 0 and e['char'] == opposite_char):
                success += 1

        print("success / len(examples)", success, "/", len(examples), "=", float(success) / len(examples))
        return float(success) / len(examples)

    def save_weights(self, filename):
        """Draws a 28x28 grayscale picture of the weights

        :param filename: Name of the file where weights will be saved
        """
        pixels = [.01 + .98 / (1.0 + float(math.exp(-w))) for w in self.weights]

        Image.fromarray(np.array(pixels).reshape(IMAGE_SIZE, IMAGE_SIZE), mode = "L").save(filename)
