"""Shifting letters."""


def encode(message: str, key: int) -> str:
    """Shifting letters."""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    new_message = ""
    for char in message:
        index = alphabet.find(char)
        if index == -1:
            new_message += char
            continue
        index += key
        index %= 26
        new_char = alphabet[index]
        new_message += new_char
    return new_message


if __name__ == '__main__':
    print(encode("i like turtles", 6))  # -> o roqk zaxzrky
    print(encode("o roqk zaxzrky", 20))  # -> i like turtles
    print(encode("example", 1))  # -> fybnqmf
    print(encode("don't change", 0))  # -> don't change
    print(encode('the quick brown fox jumps over the lazy dog.', 7))  # -> aol xbpjr iyvdu mve qbtwz vcly aol shgf kvn.
