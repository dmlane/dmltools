""" Fetch a batch of mp3 podcast files from Dropbox. """
import glob
import os
import shutil

import eyed3

from dmltools import NC, YELLOW
from dmltools.utils import error, get_dropbox_folder_location

DROPBOX_HOME = get_dropbox_folder_location()

# For car_podcasts
POD_SOURCE = f"{DROPBOX_HOME}/OnDemand/Podcasts/mp3"  # Which folder contains the podcast files
POD_DEST = os.path.expanduser("~/Work/Podcasts4IOS")  # Where to put the podcast files
POD_BATCH_HOURS = 12  # How many hours to process in abatch the podcast files


class CarPodcasts:
    """This class is responsible for fetching mp3 podcast files from Dropbox."""

    def __init__(self, source_dir=None, dest_dir=None, batch_hours=None, test_mode=False):
        self.source = source_dir or POD_SOURCE
        self.dest = dest_dir or POD_DEST

        self.batch_seconds = (batch_hours or POD_BATCH_HOURS) * 3600
        self.prefix_length = len(self.source) + 1
        self.test_mode = test_mode

    def verify_locations(self):
        """Check that our folders exist"""
        if not os.path.exists(self.source):
            error(f"Source folder {self.source} does not exist")
        if not os.path.exists(self.dest):
            error(f"Destination folder {self.dest} does not exist")

    def get_eligible_files(self):
        """Get a sorted list of mp3 podcast files"""
        self.verify_locations()

        # Get a list of all the files in the source folder
        eligible_files = glob.glob(f"{self.source}/*/*.mp3")

        # Order the files alphabetically (ignoring the directory)
        eligible_files.sort(key=os.path.basename)
        return eligible_files

    def fetch_podcasts(self):
        """Fetch the mp3 podcasts from Dropbox"""
        total_duration = 0

        # Loop over the files until we reach hour batch size
        for file_name in self.get_eligible_files():
            dest_file = self.dest + "/" + os.path.basename(file_name)

            # We cannot determine the duration of the file if it is cloud-only,
            # so we copy it to the target folder and remove it again if
            # the total exceeds our limit
            print(f"Copying {YELLOW}{file_name}{NC} ")
            shutil.copy(file_name, dest_file)
            duration = eyed3.load(dest_file).info.time_secs
            print(f"{duration} seconds")
            total_duration += duration
            if total_duration >= self.batch_seconds:
                os.remove(dest_file)
                break
            if not self.test_mode:
                os.remove(file_name)
