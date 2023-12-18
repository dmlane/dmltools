"""System static utilities being used by the modules."""
# import base64
# import os
import sys


def error(message):
    """
    Throw an error with the given message and immediately quit.

    Args:
        message(str): The message to display.
    """
    fail = "\033[91m"
    end = "\033[0m"
    sys.exit(f"{fail}Error: {message}{end}")


# def get_dropbox_folder_location():
#     """
#     Try to locate the Dropbox folder.
#
#     Returns:
#         (str) Full path to the current Dropbox folder
#     """
#     # pylint: disable=unspecified-encoding
#     host_db_path = os.path.join(os.environ["HOME"], ".dropbox/host.db")
#     try:
#         with open(host_db_path, "r") as f_hostdb:
#             data = f_hostdb.read().split()
#     except IOError:
#         # error(constants.ERROR_UNABLE_TO_FIND_STORAGE.format(provider="Dropbox install"))
#     dropbox_home = base64.b64decode(data[1]).decode()
#
#     return dropbox_home


class CustomError(Exception):
    """Custom exception"""
