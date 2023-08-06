#!/usr/bin/python

# https://opensourceseo.org/find-list-old-urls-domain-using-wayback-cdx-api/
# https://web.archive.org/web/20090420095939/https://twitter.com/realDonaldTrump
# https://web.archive.org/cdx/search/cdx?url=twitter.com/realDonaldTrump
# https://archive.org/web/researcher/cdx_file_format.php
# https://support.archive-it.org/hc/en-us/articles/115001790023-Access-Archive-It-s-Wayback-index-with-the-CDX-C-API

# Format Of Files
# ---------------
# Canonized URL
# Date
# Original URL
# Mime Type of Original Document
# Response Code
# Old Style Checksum
# Length

# Example Command
# curl "https://web.archive.org/cdx/search/cdx?url=twitter.com/realDonaldTrump" > realDonaldTrump.url

# Generate Commands
# dolt sql -q "select concat('curl \"https://web.archive.org/cdx/search/cdx?url=twitter.com/', twitter_handle, '\" > ', twitter_handle, '.url') as commands from total_tweets;" -r csv > urls.csv

# 20090420095939
# For Unmodified Pages - https://web.archive.org/web/20090420095939id_/http://twitter.com:80/realDonaldTrump
# May Want Modified Pages For Media

# For Tweet 1346928882595885058
# https://web.archive.org/web/20210106212653/https://video.twimg.com/ext_tw_video/1346928794456776705/pu/vid/1280x720/xJsJiUTRa-ggqL1D.mp4

import os
from typing import Optional

import pandas as pd
import requests

list_folder: str = "working/archive-me"
temp_files: list = os.listdir(list_folder)
files: list = []

# Remove Non-URL Files
for file in temp_files:
    if ".url" in file:
        files.append(file)

if not os.path.exists('working/wayback'):
    os.makedirs('working/wayback')

for file in files:
    download_folder_stripped: str = str(file).rstrip(".url")
    download_folder: str = os.path.join('working/wayback', download_folder_stripped)
    if not os.path.exists(download_folder):
        print(f"Creating: {download_folder}")
        os.makedirs(download_folder)

    print(f"Downloading Archives For {download_folder_stripped}")

    contents: pd.DataFrame = pd.read_csv(filepath_or_buffer=os.path.join(list_folder, file),
                                         header=None,
                                         delimiter=" ",
                                         usecols=[0, 1, 2, 3, 4, 5, 6],
                                         names=["canonized_url",
                                                "date",
                                                "original_url",
                                                "mime_type",
                                                "response_code",
                                                "old_checksum",
                                                "length"])

    # https://web.archive.org/web/20090420095939id_/http://twitter.com:80/realDonaldTrump
    contents["raw_url"] = "https://web.archive.org/web/" + contents["date"].astype(str) + "id_/" + contents["original_url"].astype(str)
    contents["archive_url"] = "https://web.archive.org/web/" + contents["date"].astype(str) + "/" + contents["original_url"].astype(str)

    print(contents)
    contents.to_csv(path_or_buf=os.path.join(list_folder, download_folder_stripped + ".csv"))

    contents.drop_duplicates(inplace=True, subset=["old_checksum"])

    # Headers
    headers: dict = {
        'User-Agent': 'Chrome/90',  # python-requests/2.25.1
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }

    total: int = len(contents.index)
    count: int = 1
    for row in contents.itertuples():
        # TODO: Means To Skip Already Downloaded Files (Doesn't Handle Multiple Different Files On Same Date)
        # if os.path.exists(os.path.join(download_folder, str(row.date) + "-archive.html")):
        #     print(f"Page {count}/{total} - Skipping {row.date} From {download_folder_stripped}")
        #     count += 1
        #     continue

        try:
            if not os.path.exists(os.path.join(download_folder, str(row.date) + "-raw.html")):
                # https://twitter.com/AlexisEvelyn42/status/1350405163048169475
                r = requests.get(row.raw_url, allow_redirects=True, headers=headers)

                r_page = open(mode="w", file=os.path.join(download_folder, str(row.date) + "-raw.html"))
                r_page.writelines(r.text)
                r_page.close()
                print(f"Raw Page {count}/{total} - Saved {row.date} From {download_folder_stripped}")
            else:
                print(f"Raw Page {count}/{total} - Skipping {row.date} From {download_folder_stripped}")
        except:
            print(f"Failed To Download Raw Page!!! Logging!!! Page: {download_folder_stripped}/{row.date}")
            failed_log = open(mode="a", file='working/wayback/failed-download.txt')
            failed_log.writelines(f"Raw - {download_folder_stripped}/{row.date}\n")
            failed_log.close()

            # exit(1)

        try:
            if not os.path.exists(os.path.join(download_folder, str(row.date) + "-archive.html")):
                a = requests.get(row.archive_url, allow_redirects=True, headers=headers)

                a_page = open(mode="w", file=os.path.join(download_folder, str(row.date) + "-archive.html"))
                a_page.writelines(a.text)
                a_page.close()
                print(f"Archive Page {count}/{total} - Saved {row.date} From {download_folder_stripped}")
            else:
                print(f"Archive Page {count}/{total} - Skipping {row.date} From {download_folder_stripped}")
        except:
            print(f"Failed Connection!!! Page: {download_folder_stripped}/{row.date}")
            failed_log = open(mode="a", file='working/wayback/failed-download.txt')
            failed_log.writelines(f"Archive - {download_folder_stripped}/{row.date}\n")
            failed_log.close()

            # exit(1)

        # print(f"Page {count}/{total} - Saved {row.date} From {download_folder_stripped}")
        count += 1
