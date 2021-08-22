import time
import random
import sys
import re
from pathlib import Path
import argparse
import json

from archivenow import archivenow


def run():
    url_regex = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

    parser = argparse.ArgumentParser(
        description="Archive websites listed inside a file. The file does not need to follow any specific format."
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        help="File to output all urls to",
    )
    parser.add_argument(
        "-d",
        "--delay",
        type=int,
        dest="delay",
        default=4,
        help="Delay between processing each URL in seconds",
    )
    parser.add_argument(
        "file",
        metavar="file",
        type=str,
        help="Path to the file containing the urls to archive",
    )
    args = parser.parse_args()

    file = Path(args.file).absolute()

    if args.output_file:
        output_file = Path(args.output_file).with_suffix(".json").absolute()
        if output_file.exists():
            sys.exit(f"The file {output_file} does already exist")

    with open(file) as f:
        text = f.read()
    urls = re.findall(url_regex, text)
    # Randomize urls to archive different urls on every program run,
    # even if the program doesn't finish.
    random.shuffle(urls)

    results = dict()
    for url in urls:
        results[url] = archivenow.push(url, "ia")
        time.sleep(args.delay)

    if args.output_file:
        with open(output_file, "w") as f:
            f.write(json.dumps(results, indent=2))
