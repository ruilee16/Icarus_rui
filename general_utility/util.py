from os import walk


def read_files_in_dir(folder_location: str) -> list:
    """
    give the dictionary, return the files in the dictionary. This function is used for batch read MRT data.
    :param folder_location: give the folder url
    :return: list of files in the folder url
    """
    files = next(walk(folder_location), (None, [], None))[1]
    return [file for file in files]



