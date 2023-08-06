"""
dzcb.pnwdigital - cache data from PNWDigital.net
"""
import argparse
import logging
from pathlib import Path
import os
import tempfile
from zipfile import ZipFile

import requests

logger = logging.getLogger(__name__)

PNWDIGITAL_REPEATERS = "http://www.pnwdigital.net/files/acb/PNW_Digital_Repeaters.zip"
REPEATER_FILENAME = "Digital-Repeaters__PNWDigital.csv"
TALKGROUPS_FILENAME = "Talkgroups__PNWDigital.csv"


def cache_repeaters(output_dir):
    resp = requests.get(PNWDIGITAL_REPEATERS)
    resp.raise_for_status()
    with tempfile.TemporaryFile() as tf:
        tf.write(resp.content)
        zf = ZipFile(tf, "r")
        names = zf.namelist()
        zip_repeater_filename = [
            n for n in names if n.startswith("Digital-Repeaters__PNW-all")
        ]
        if len(zip_repeater_filename) > 1:
            raise RuntimeError(
                "Multiple Digital-Repeaters found in the zip: {}".format(
                    zip_repeater_filename
                )
            )
        output_repeaters = Path(output_dir) / REPEATER_FILENAME
        output_repeaters.write_bytes(zf.read(zip_repeater_filename[0]))
        logger.info("Cache PNWDigital k7abd zones to '%s'", output_repeaters)

        zip_talkgroups_filename = [
            n for n in names if n.startswith("Talkgroups__PNW-all")
        ]
        if len(zip_talkgroups_filename) > 1:
            raise RuntimeError(
                "Multiple Talkgroups found in the zip: {}".format(
                    zip_talkgroups_filename
                )
            )
        output_talkgroups = Path(output_dir) / TALKGROUPS_FILENAME
        output_talkgroups.write_bytes(zf.read(zip_talkgroups_filename[0]))
        logger.info("Cache PNWDigital k7abd talkgroups to '%s'", output_talkgroups)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir")
    args = parser.parse_args()
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    cache_repeaters(args.output_dir)
