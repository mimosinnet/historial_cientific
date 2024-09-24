import json
from os.path import isfile
from pyzotero import zotero
from .common import sort_refs
from .global_variables import LIBRARY, API_ID, API_KEY, CACHE_PATH, HISTORIAL, config
from .reference import Reference
from .reference_atoms import Date


class Collection:
    def __init__(self, id, latex):
        self.id = id  # library key
        self.latex = latex
        self.years = config["years"]
        self.section = config["keys"][id]
        self.collection = config["coll_keys"][id]
        self.types = config["section"][self.section]["types"]
        self.file = CACHE_PATH + self.id + ".json"
        # Zotero credentials
        self.library = LIBRARY
        self.api_id = API_ID
        self.api_key = API_KEY
        self.items = self.get_items()

    # download_collection #<
    def download_collection(self):
        print(f"Downloading key {self.id}: {self.collection}: ")
        zot = zotero.Zotero(self.api_id, self.library, self.api_key)

        print(self.file)
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(zot.everything(zot.collection_items(self.id)), f)

    # #>

    # get items #<
    def get_items(self):
        years = self.years
        id = self.id
        # print(id)

        if not isfile(self.file):
            self.download_collection()

        with open(self.file, "r", encoding="utf-8") as f:
            items = json.load(f)

        # print(items[0])

        selected = []
        for i in items:
            itemType = i["data"]["itemType"]
            # print(itemType)
            year = Date(i["data"].get("date", "")).get_year()
            # print(year)

            if (
                # Col·leccions que no son escollides per data
                id == "36U9M8UA"  # current projects
                or id == "N7K6GRL2"  # previos Projects
                or id == "FYCMV3HK"  # Participation in International Networks
                or id == "YUGQZ453"  # Doctoral thesis in progress
                or id == "3HN4HS2I"  # Post-Doctoral Grants
                or id == "TZFYNY2Y"  # Pre-Doctoral Grants
                or id == "QR2SVS4L"  # Podcasts
            ):
                selected.append(i["data"])
            elif year == "No Year":
                continue
            elif (itemType in self.types) and (int(year) in range(years[0], years[1])):
                # print("yes")
                selected.append(i["data"])
            else:
                continue

        return selected

    # #>

    # get_reg0: get first register #<
    def get_reg0(self):
        item = self.items
        print(f"Dictionary for collection {self.id}: {self.collection}")
        # print(item)
        # exit()
        for i in item[0].keys():
            try:
                print(i, item[0][i], sep=": ")
            except IndexError:
                pass  # #>

    # get creators #<
    def get_creators(self):
        creators = []
        for i in self.items:
            creators.append(i["creators"])

        return creators

    # #>

    # get authors #<
    def get_authors(self):
        authors = []
        for i in self.items:
            author = Author(i["creators"])
            if self.id == "QR2SVS4L":  # podcast
                author.auth_type = "podcaster"
            authors.append(author.get_auth())

        return authors

    # #>

    # get editors #<
    def get_editors(self):
        authors = []
        for i in self.items:
            creators = Author(i["creators"])
            authors.append("Author: " + creators.get_auth())
            creators.auth_type = "editor"
            authors.append("Editor: " + creators.get_auth())

        return authors

    # #>

    # get years #<
    def get_years(self):
        years = []
        for i in self.items:
            try:
                year = Date(i["date"])
                years.append(f"{year.get_year()}, {year.get_date()}")
            except KeyError:
                years.append(f"No date field in collection: {self.collection}")

        return years

    # #>

    # get titles #<
    def get_titles(self):
        titles = []
        for i in self.items:
            titles.append(i["title"])

        return titles

    # #>

    # get journals #<
    def get_journals(self):
        journals = []
        for i in self.items:
            journal_title = i["publicationTitle"]
            volume = i["volume"]
            issue = i["issue"]
            pages = i["pages"]
            journal = Journal(journal_title, volume, issue, pages)
            journals.append(journal.get_journal())
        return journals

    # #>

    # get_refs #<
    def get_refs(self):
        refs = {}
        num = 0
        for i in self.items:
            num += 1
            itemType = i["itemType"]
            match itemType:
                case "journalArticle":
                    ref = Reference(self.id, i, num, self.latex).get_article_selector()
                    refs.update(ref)
                case "book":
                    ref = Reference(self.id, i, num, self.latex).get_book()
                    refs.update(ref)
                case "bookSection":
                    ref = Reference(self.id, i, num, self.latex).get_book_chapter()
                    refs.update(ref)
                case "conferencePaper":
                    ref = Reference(self.id, i, num, self.latex).get_conference_paper()
                    refs.update(ref)
                case "thesis":
                    ref = Reference(self.id, i, num, self.latex).get_thesis()
                    refs.update(ref)
                case "presentation":
                    # Organization of international conferences
                    ref = Reference(self.id, i, num, self.latex).get_presentation()
                    refs.update(ref)
                case "report":
                    ref = Reference(self.id, i, num, self.latex).get_report()
                    refs.update(ref)
                case "thesis":
                    ref = Reference(self.id, i, num, self.latex).get_thesis()
                    refs.update(ref)
                case "magazineArticle":
                    ref = Reference(self.id, i, num, self.latex).get_magazine()
                    refs.update(ref)
                case "podcast":
                    ref = Reference(self.id, i, num, self.latex).get_podcast()
                    refs.update(ref)
                case "tvBroadcast":
                    ref = Reference(self.id, i, num, self.latex).get_tv()
                    refs.update(ref)
                case "blogPost":
                    ref = Reference(self.id, i, num, self.latex).get_blog()
                    refs.update(ref)
                case _:
                    print("Error appending item ", i)
        return sort_refs(refs)

    # #>

    # write_refs #<
    def write_refs(self):
        refs = self.get_refs()
        file = HISTORIAL + self.id + ".tex"
        print("Writting to " + file)
        with open(file, "w", encoding="utf-8") as f:
            f.writelines(
                [
                    "% " + self.section + " {{{",
                    "\n",
                    "\\begin{enumerate}",
                    "\n",
                ]
            )

            for item in refs:
                f.write(item.replace("&", "\\&").replace("_", "\\_") + "\n")

            f.writelines(["\\end{enumerate}", " \n", "% }}}", "\n"])

    # #>


# vim: foldmarker=#<,#>
