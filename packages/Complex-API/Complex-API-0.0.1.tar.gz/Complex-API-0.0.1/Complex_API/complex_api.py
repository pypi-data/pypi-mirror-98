import requests

API_URL = "https://complicated-api.herokuapp.com/"
GITHUB_REPO = "https://github.com/JagTheFriend/Complex-API"

__version__ = "1.1.1"
__all__ = [
    "compile", "reddit", "lyrics",
    "ascii", "temp", "length",
    "inspire", "calculator", "hex_to_denary"
]


def main() -> str:
    return requests.get(f"{API_URL}").text


def compile(*, lang, code) -> dict:
    """
    Gets the result of compiling code from the `Compiler API`
    :param lang: The language which the compiler would use to compile code
    :param code: The code to be compiled
    :return: Dictionary
    """
    return requests.get(f"{API_URL}/compile={lang}_{code}").json()


def reddit(*, limit: float, subreddit: str) -> dict:
    """
    Gets a limited amount of posts from a specific subreddit
    :param subreddit: Name of the subreddit
    :param limit: Number of posts to be returned
    :return: Dictionary
    """
    return requests.get(f"{API_URL}/reddit={subreddit}+{limit}").json()


def lyrics(*, song: str) -> dict:
    """
    Gets the lyrics of a song from the `Lyrics API`
    :param song: Name of the song
    :return: Dictionary
    """
    return requests.get(f"{API_URL}/lyrics+{song}").json()


def ascii(*, text) -> dict:
    """
    Gets Pixel art from the ASCII API
    :param text: The text which should be converted to Pixel art
    :return: Dictionary
    """
    return requests.get(f"{API_URL}/ascii_{text}").json()


def temp(*, place) -> dict:
    """
    Gets the weather of a place
    :param place: The name of the place whose weather would be found
    :return: Dictionary
    """
    return requests.get(f"{API_URL}/temp={place}").json()


def length(*, playlist: str) -> dict:
    """
    Gets the length of playlist
    :param playlist: This a unique id given to each playlist
    :return: Dictionary
    """
    return requests.get(f"{API_URL}/length+{playlist}").json()


def inspire() -> dict:
    """
    Gets a random inspirational text
    :return: Dictionary
    """
    return requests.get(f"{API_URL}/inspire").json()


def calculator(*, formula: str) -> dict:
    """
    Gets the result of a calculation
    :param formula: Stuff on which calculation will be carried on Example: 5+7*9
    :return: Dictionary
    """
    return requests.get(f"{API_URL}/cal_{formula}").json()


def hex_to_denary(*, hex_code) -> dict:
    """
    Converts Hexadecimal code to decimal(or denary)
    :param formula: Stuff on which calculation will be carried on Example: 5+7*9
    :return: Dictionary
    """
    return requests.get(f"{API_URL}/hex_to_denary+{hex_code}").json()
