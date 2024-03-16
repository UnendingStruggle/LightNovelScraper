import os
import time
from pathlib import Path
from lightnovelscraper import SearchFunction, ChapterScrape, ChapterDownloadFunction, remove_special_characters
# global variables:
# FinalPath
# LightNovelName
# ChoosenNovel
# Choice
# ChapterLinks

# List of sources for light novel scraping
Sources = ["https://novelbin.hotnovelpub.net/",
           "https://novelbin.app/"]

# Function to choose a source for downloading the light novel


def SourceChoosing():
    try:
        for i in Sources:
            print("\n", "[", Sources.index(i)+1, "]", i, sep="")
        global Choice
        Choice = int(
            input("\n\033[0;32mChoose a source for downloading Light Novel: \033[0;37m"))
    except:
        print("\033[0;31mInvalid Input. Try Again.\033[0;37m")
        time.sleep(2)
        print("\n")
        SourceChoosing()
    else:
        if 0 < Choice <= len(Sources):
            NovelTitles = SearchFunction(Sources[Choice-1], LightNovelName)
            SeriesListing(NovelTitles)
        else:
            print("\033[0;31mInput outside the range. Try again.\033[0;37m")
            time.sleep(2)
            print("\n")
            SourceChoosing()

# Function to list the available series of the chosen light novel


def SeriesListing(NovelTitles):
    if len(NovelTitles) == 0:
        print("\033[0;31mThere were no results. Please search again\033[0;37m")
        time.sleep(2)
        print("\n")
        initiate()
    else:
        for i in NovelTitles:
            print("[", NovelTitles.index(i)+1, "]", i[0], sep="")
        try:
            Choice = int(input("\n\033[0;32mChoose a Light Novel: \033[0;37m"))
        except:
            print("\033[0;31mInvalid Input. Try again.\033[0;37m", end='')
            time.sleep(2)
            print("\n")
            SeriesListing(NovelTitles)
        else:
            if 0 < Choice <= len(NovelTitles):
                try:
                    global ChoosenNovel
                    global chapter_index
                    global ChapterLinks
                    ChoosenNovel = NovelTitles[Choice-1]
                    print(ChoosenNovel[0])
                    print(f"Latest Chapter: {ChoosenNovel[3]}")
                    print("\033[1;32m \nDownloading Links.\033[0;37m", end='')
                    ChapterLinks = ChapterScrape(ChoosenNovel)
                    index_choosing()
                except:
                    print("\033[0;31mConnection Error. Try again.\033[0;37m")
                    time.sleep(2)
                    print("\n")
                    SeriesListing(NovelTitles)

            else:
                print("\033[0;31mInput outside the range. Try again.\033[0;37m")
                time.sleep(2)
                print("\n")
                SeriesListing(NovelTitles)

# Function to enter index of chapters to download


def index_choosing():
    try:
        chapter_index = list(map(int, input(
            "\033[0;32mEnter index of chapter(s) to download (example: 12-43 MAX(25)): \033[0;37m").split("-")))
    except:
        print(
            "\033[0;31mInvalid Input. Try again.\033[0;37m")
        time.sleep(2)
        index_choosing()
    else:
        try:
            if (0 < chapter_index[0] <= len(ChapterLinks) and 0 < chapter_index[1] <= len(ChapterLinks)):
                DownloadingFunction(chapter_index)
        except:
            print(
                "\033[0;31mInvalid Input. Try again.\033[0;37m")
            time.sleep(2)
            index_choosing()

# Function to download chapters of the light novel


def DownloadingFunction(chapter_index):
    global FinalPath
    DownloadPath = str(Path.home() / "Downloads")
    FinalPath = os.path.join(
        DownloadPath, remove_special_characters(ChoosenNovel[0]))
    PermError = 0
    try:
        os.mkdir(FinalPath)
        print("\033[0;32m\nFolder created with path %s.\033[0;37m\n" % FinalPath)
    except FileExistsError:
        print("\033[0;32m\nFolder Exists at %s.\033[0;37m\n" % FinalPath)
        pass
    except PermissionError:
        print("\033[0;31mInsufficient Permissions to make a folder in that location. Please enter a new path\033[0;37m")
        time.sleep(2)
        print("\n")
        PermError = 1
        pass
    finally:
        if PermError == 1:
            DownloadingFunction(chapter_index)
        else:
            ChapterDownloadFunction(ChapterLinks, chapter_index, FinalPath)
            raise SystemExit(
                "\033[0;32m\nAll Files Downloaded Successfully\033[0;37m")

# Function to initiate the light novel download process


def initiate():
    global LightNovelName
    print("\033[1;32m \nWaiting for Cloudfare... \033[0;37m \n")
    time.sleep(2)
    LightNovelName = input(
        "\033[0;32mEnter The Name of Light Novel you wish to download: \033[0;37m")
    print("\n\033[1;32mFetching Sources...\033[0;37m ")
    time.sleep(2)
    SourceChoosing()


initiate()
