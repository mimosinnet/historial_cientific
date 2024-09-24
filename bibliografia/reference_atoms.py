import re
import datetime  # strftime
from .common import neteja, get_date_object


# Class Authors #<
class Author:
    def __init__(self, creators):
        self.creators = creators
        self.auth_type = "author"

    # def get_auth #<
    def get_auth(self):
        creator = self.creators
        auth_type = self.auth_type

        author = str("NoAutor")
        if len(creator) == 0:
            return author

        author = ""
        for i in range(len(creator)):

            if creator[i]["creatorType"] != auth_type:
                continue
            else:
                item = creator[i]
                name = item.get("name", "")
                firstName = item.get("firstName", "")
                lastName = item.get("lastName", "")

                # Han posat cognom, nom en el cognom
                if firstName == "" and lastName != "":
                    name = lastName

                if name != "":
                    name_array = name.split(",")
                    if len(name_array) == 2:
                        firstName = name_array[1].strip()
                        lastName = name_array[0].strip()
                    else:
                        lastName = name_array[0].strip()

                if lastName != "":
                    lastName += ", "

                author_name = ""
                if auth_type == "editor":
                    author_name = firstName + " " + lastName
                else:
                    author_name = lastName + firstName

                if auth_type == "editor":
                    author += author_name
                else:
                    author += author_name + "; "

        return neteja(author)

    # ♯>

    def get_author(self):
        self.auth_type = "author"
        author = self.get_auth()
        return author

    def get_editor(self):
        self.auth_type = "editor"
        author = self.get_auth()
        return author

    # #>

    # #>


class Date:  # #<
    def __init__(self, date1, date2=None):
        self.date1 = date1
        self.date2 = date2

    def get_year(self):  # #<
        valid_year = re.compile(r"\b(19|20)\d{2}\b")
        m = valid_year.search(self.date1)
        if m:
            return m.group(0)
        else:
            return "No Year"  # #>

    def get_date(self):  # #<
        date_obj = get_date_object(self.date1)
        try:
            return date_obj.strftime("%d %B %Y")
        except AttributeError:
            pass

        return "NoDate"  # #>

    def get_date_range(self):  # #<
        if self.date2:
            try:
                date_obj1 = get_date_object(self.date1)
                date_obj2 = get_date_object(self.date2)
                return f"{date_obj1.strftime('%d')}-{date_obj2.strftime('%d %B %Y')}"
            except ValueError:
                return "NoDate"
        else:
            return ""  # #>

    def get_date_range_project(self):  # #<
        if self.date2:
            try:
                date_obj1 = get_date_object(self.date1)
                date_obj2 = get_date_object(self.date2)
                return f"From {date_obj1.strftime('%B-%Y')} to {date_obj2.strftime('%B-%Y')}"
            except ValueError:
                return "NoDate"
        else:
            return ""  # #>


# #>


# Class JournalDetails #<
class JournalDetails:
    def __init__(self, volume, issue, pages):
        self.volume = volume
        self.issue = issue
        self.pages = pages

    def get_journal_details(self):
        volume = self.volume
        issue = self.issue
        pages = self.pages
        if volume + issue + pages == "":
            return ""
        if (volume != "") and (issue != ""):
            issue = "(" + issue + ")"
        if pages != "":
            pages = ", " + pages

        return volume + issue + pages + ". "


# #>


# Class Impact #<
class Impact:
    def __init__(self, jif, q_jrc, sjr, citations):
        self.jif = jif
        self.q_jrc = q_jrc
        self.sjr = sjr
        self.citations = citations

    def get_impact(self):
        jif = self.jif
        jrc = self.q_jrc
        sjr = self.sjr
        citations = self.citations

        jcr_inx = ""
        sjr_inx = ""
        cit_inx = ""
        if jif != "":
            jcr_inx = f"JCR: {jif}: {jrc}.  "
        if sjr != "":
            sjr_inx = f"{sjr}. "
        if citations != "":
            cit_inx = f"Citations: {citations}. "

        return jcr_inx + sjr_inx + cit_inx


# #>

# vim: foldmarker=#<,#>
