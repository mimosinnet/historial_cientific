from .common import completar, neteja, concat
from .global_variables import ITEM, FILBREAK
from .reference_atoms import Author, Date, JournalDetails, Impact


class Reference:
    def __init__(self, id, item, item_number, latex):
        self.id = id
        self.item = item
        self.item_number = item_number
        self.latex = latex

    # get_article #<
    def get_art(self):
        item = self.item

        author = Author(item["creators"]).get_author()
        year = Date(item["date"]).get_year()
        journal_title = item["publicationTitle"]
        volume = item["volume"]
        issue = item["issue"]
        pages = item["pages"]
        journal_details = JournalDetails(volume, issue, pages).get_journal_details()

        # impact #<
        jif = item["archive"]
        jrc = item["archiveLocation"]
        sjr = item["libraryCatalog"]
        citations = item["callNumber"]
        impact = Impact(jif, jrc, sjr, citations).get_impact()
        # #>

        doi = ""
        if item["DOI"] != "":
            # \\ = new line in latex
            doi = "\\\\ DOI: " + item["DOI"] + ". "

        match self.id:
            case "UWPY76KY":  # Indexed Articles
                if self.latex:
                    ref = f'{{\\bf {year}}}: {author}.  {item["title"]}. {{\\it {journal_title}}}, {journal_details}{{\\bf Index: {impact}}} {doi}'
                    ref = ITEM + ref + FILBREAK
                else:
                    ref = f'{year}: {author}. {item["title"]}. {journal_title}, {journal_details}{doi}Index: {impact}'
            case "442HYH2P":  # Non-Idexed Articles
                if self.latex:
                    ref = f'{{\\bf {year}}}: {author}.  {item["title"]}. {{\\it {journal_title}}}, {journal_details} {doi}'
                    ref = ITEM + ref + FILBREAK
                else:
                    ref = f'{year}: {author}. {item["title"]}. {journal_title}, {journal_details} {doi}'
            case _:
                print("error")

        ref = {year + author + str(self.item_number): ref}

        return ref

    # #>

    def get_project(self):  # #<
        # 36U9M8UA: current projects
        # N7K6GRL2: previos projects
        # BRL62EC2: Competitive Transfer Grants
        item = self.item
        years = item["pages"]
        title = item["title"]
        investor = item["publicationTitle"]
        reference = item["DOI"]
        budget = item["extra"]
        date_range = Date(item["accessDate"], item["archive"]).get_date_range_project()
        author = Author(item["creators"]).get_author()

        if budget != "":
            budget = f"Budget: {budget}."

        if self.latex:
            ref = f"{{\\bf {years}}}. {{\\it {title}}}. {{\\bf {investor}}}, {date_range} reference: {reference}. {{\\bf  {budget}}} Principal Investigator: {{\\bf {author}}}."
            ref = ITEM + ref + FILBREAK
        else:
            ref = f"{years}: {title}. {investor}, {date_range} reference: {reference}. {budget} Principal Investigator: {author}."

        ref = {years + author + str(self.item_number): ref}

        return ref

    # #>

    def get_grant(self):  # #<

        item = self.item
        year = Date(item["date"]).get_year()
        author = Author(item["creators"]).get_author()
        ayuda = item["title"]
        institution = item["publicationTitle"]
        years = item["pages"]
        date_range = Date(item["accessDate"], item["archive"]).get_date_range_project()
        duration = years + date_range
        concatenate = concat(", ", ".", institution, duration)

        if self.latex:
            ref = f"{{\\bf {year}}}. {author}. {{\\bf {ayuda}}}{concatenate}"
            ref = ITEM + ref + FILBREAK
        else:
            ref = f"{year}. {author}. {ayuda}{concatenate}."

        ref = {year + author + str(self.item_number): ref}

        return ref  # #>

    # get_book #<
    def get_book(self):
        item = self.item
        author = Author(item["creators"]).get_author()
        year = Date(item["date"]).get_year()
        title = item["title"].strip()
        place = completar(item["place"].strip())
        publisher = completar(item["publisher"].strip())
        impacto = item["extra"]
        if impacto != "":
            impacto = f"Impacto: {impacto}. "

        if self.latex:
            ref = f"{{\\bf {year}}}: {author}. {{\\it {title}}}. {place}: {publisher}."
            ref = ITEM + ref + FILBREAK
        else:
            ref = f"{year}: {author}. {title}. {place}: {publisher}. {impacto}"

        ref = {year + author + str(self.item_number): ref}

        return ref

    # #>

    # get_book_chapter #<
    def get_book_chapter(self):
        item = self.item
        creators = Author(item["creators"])
        author = creators.get_author()
        editor = creators.get_editor()
        year = Date(item["date"]).get_year()
        title = item["title"].strip()
        bookTitle = item["bookTitle"].strip()
        place = completar(item["place"].strip())
        publisher = completar(item["publisher"].strip())
        pages = item["pages"]
        impacto = item["extra"]
        if impacto != "":
            impacto = f"Impact: {impacto}."

        if self.latex:
            ref = f"{{\\bf {year}}}: {author}. {title}. {{\\bf In}} {editor} (Ed.): {{\\it {bookTitle}}} (pp. {pages}). {place}: {publisher}. {{\\bf {impacto}}}"
            ref = ITEM + ref + FILBREAK
        else:
            ref = f"{year}: {author}. {title}. In {editor} (Ed.): {bookTitle} (pp. {pages}). {place}: {publisher}. {impacto}"

        ref = {year + author + str(self.item_number): ref}

        return ref

    # #>

    def get_conference_paper(self):  # #<
        item = self.item
        year = Date(item["date"]).get_year()
        author = Author(item["creators"]).get_author()
        title = item["title"]
        conferenceName = item["conferenceName"]
        place = item["place"]
        conference_date = Date(item["accessDate"], item["archive"]).get_date_range()
        concatenate = concat(". ", ".", conferenceName, conference_date, place)

        if self.latex:
            ref = f"{{\\bf {year}}}: {author}. {{\\it {title}}}{concatenate}"
            ref = ITEM + ref + FILBREAK
        else:
            ref = f"{year}: {author}. {title}{concatenate}"

        ref = {year + author + str(self.item_number): ref}

        return ref  # #>

    # get_presentation #<
    def get_presentation(self):
        # org. international conferences
        item = self.item
        title = item["title"]
        conf_type = item["presentationType"]
        date = item["date"]
        year = Date(date).get_year()
        place = item["place"]
        organizer = item["meetingName"]

        if self.latex:
            ref = f"{{\\bf {year}}}. {{\\it {title}}}, {place}, {date}. Organized by {organizer}. {{\\bf {conf_type}}}."
            ref = ITEM + ref + FILBREAK
        else:
            ref = f"{year}. {title}, {place}, {date}. Organized by {organizer}. {conf_type}."

        ref = {year + title + str(self.item_number): ref}

        return ref

    # #>

    # get_report #<
    def get_report(self):
        # Participation in International Networks
        item = self.item
        date = item["date"]
        year = Date(date).get_year()
        years = item["pages"]
        author = Author(item["creators"]).get_author()
        title = item["title"]
        department = item["seriesTitle"]
        institution = neteja(item["institution"])
        place = neteja(item["place"])
        date_range = Date(item["accessDate"], item["archive"]).get_date_range()
        duration = years + date_range
        supervisor = item["extra"]
        concatenate = concat(", ", ".", department, institution, place, duration)

        if self.id == "FYCMV3HK":  # Participation in International Networks"
            if self.latex:
                ref = f"{{\\bf {year}}}. {{\\it {title}}}{concatenate}"
                ref = ITEM + ref + FILBREAK
            else:
                ref = f"{year}. {title}{concatenate}"

        elif self.id == "Q5E6D3QA":  # International stages
            if self.latex:
                ref = f"{{\\bf {year}}}. {author}. {{\\it {title}}}{concatenate} {{\\bf Supervised by}}: {supervisor}"
                ref = ITEM + ref + FILBREAK
            else:
                ref = f"{{\\bf {year}}}. {author}. {{\\it {title}}}{concatenate} Supervised by: {supervisor}"

        ref = {year + author + str(self.item_number): ref}

        return ref

    # #>

    # get_thesis #<
    def get_thesis(self):
        item = self.item
        year = Date(item["date"]).get_year()
        author = Author(item["creators"]).get_author()
        title = neteja(item["title"])
        type_item = item["thesisType"]
        university = item["university"]
        department = item["archive"]
        mention = item["libraryCatalog"]
        qualification = item["callNumber"]
        programme = neteja(item["rights"])
        director = neteja(item["extra"])

        concatenate = concat(". ", ".", programme, department, university, mention)

        ref = ""
        match self.id:
            case "H9FYFWQY":  # Completed doctoral theses
                if self.latex:
                    ref = f"{{\\bf {year}}}. {author}. {{\\it {title}}}{concatenate} {{\\bf {qualification}}}. Directed by: {director}."
                    ref = ITEM + ref + FILBREAK
                else:
                    ref = f" {year}. {author}. {title}{concatenate} {qualification}. Directed by: {director}."
            case "YUGQZ453":  # Doctoral thesis in progress
                if self.latex:
                    ref = f"{{\\bf {year}}}. {author}. {{\\it {title}}}{concatenate} Directed by: {director}."
                    ref = ITEM + ref + FILBREAK
                else:
                    ref = f" {year}. {author}. {title}{concatenate} Directed by: {director}."
            case "PJNPKBEK":  # Final Master Theses
                if self.latex:
                    ref = f"{{\\bf {year}}}. {author}. {{\\it {title}}}{concatenate} Directed by: {director}."
                    ref = ITEM + ref + FILBREAK
                else:
                    ref = f" {year}. {author}. {title}{concatenate} Directed by: {director}."
            case "PWH78LJ5":  # Non-competitive contracts/agreements
                if self.latex:
                    ref = f"{{\\bf {year}}}. {{\\bf {title}}}, {{\\it {type_item}}}."
                    ref = ITEM + ref + FILBREAK
                else:
                    ref = f"{year}.  {title}, {type_item}."

        ref = {year + author + str(self.item_number): ref}

        return ref

    # #>

    # get_non_competitive_projects #<
    def get_non_competitive_projects(self):
        # Non-competitive contracts/agreements
        item = self.item
        institution = item["title"]
        agreement_type = item["thesisType"]
        year = item["date"]

        if self.latex:
            ref = f"{{\\bf {year}}}. {{\\bf {institution}}}, {{\\it {agreement_type}}}."
            ref = ITEM + ref + FILBREAK
        else:
            ref = f"{year}.  {institution}, {agreement_type}."

        ref = {year + institution + str(self.item_number): ref}

        return ref

    # #>

    def get_magazine(self):  # #<
        #  BW926N6F P5RR9R5K
        # AFIN free monthly publication
        item = self.item
        year = Date(item["date"]).get_year()
        author = Author(item["creators"]).get_author()
        title = item["title"]
        url = item["url"]
        ref = ""
        concatenate = concat(
            ", ", ".", item["publicationTitle"], item["issue"], item["pages"]
        )

        if self.latex:
            ref = f"{{\\bf {year}}}. {author}. {{\\it {title}}}{concatenate} \\\\ \\url{{ {url} }}"
            ref = ITEM + ref + FILBREAK
        else:
            ref = f"{year}. {author}. {title}{concatenate} \\\\{url}"

        ref = {year + author + str(self.item_number): ref}

        return ref  # #>

    def get_podcast(self):  # #<
        item = self.item
        date = Date(item["accessDate"])
        year = date.get_year()
        author = Author(item["creators"])
        author.auth_type = "podcaster"
        podcaster = author.get_auth()
        title = item["title"]
        concatenate = concat(
            ", ", ".", item["seriesTitle"], item["episodeNumber"], date.get_date()
        )
        url = item["url"]

        if self.latex:
            ref = f"{{\\bf {year}}}. {podcaster}. {{\\it {title}}}{concatenate} \\\\ \\url{{ {url} }}"
            ref = ITEM + ref + FILBREAK
        else:
            ref = f"{year}. {podcaster}. {title}{concatenate} \\\\{url}"

        ref = {year + podcaster + str(self.item_number): ref}

        return ref  # #>

    # get_tv #<
    def get_tv(self):
        item = self.item
        date = Date(item["date"])
        year = date.get_year()
        emitted = date.get_date()
        author = Author(item["creators"])
        author.auth_type = "director"
        director = author.get_auth()
        title = item["title"]
        program = item["programTitle"]
        url = item["url"]

        if self.latex:
            ref = f"{{\\bf {year}}}. {director}. {{\\it {title}}}, {program}, {emitted}. \\\\ \\url{{ {url} }}"
            ref = ITEM + ref + FILBREAK
        else:
            ref = f"{year}. {director}. {title}, {program}, {emitted}. \\\\{url}"

        ref = {year + director + str(self.item_number): ref}

        return ref

    # #>

    # get_blog #<
    def get_blog(self):
        item = self.item
        date = Date(item["date"])
        year = date.get_year()
        published = date.get_date()
        author = Author(item["creators"]).get_auth()
        title = item["title"]
        blog = item["blogTitle"]
        url = item["url"]

        if self.latex:
            ref = f"{{\\bf {year}}}. {author}. {{\\it {title}}}, {blog}, {published}. \\\\ \\url{{ {url} }}"
            ref = ITEM + ref + FILBREAK
        else:
            ref = f"{year}. {author}. {title}, {blog}, {published}. \\\\{url}"

        ref = {year + author + str(self.item_number): ref}

        return ref

    # #>

    # get thesis_selector #<
    def get_thesis_selector(self):
        match self.id:
            case "PWH78LJ5":
                print(self.id)
                return self.get_non_competitive_projects()
            case "H9FYFWQY" | "YUGQZ453":
                return self.get_thesis()
            case _:
                print("Error in fucntion get_thesis_selector")

    # #>

    # get_article selector #<
    def get_article_selector(self):
        match self.id:
            case "UWPY76KY" | "442HYH2P":  # Articles
                return self.get_art()
            case "36U9M8UA" | "N7K6GRL2" | "BRL62EC2":  # Projects
                return self.get_project()
            case "3HN4HS2I" | "TZFYNY2Y":  # grants
                return self.get_grant()
            case _:
                print("Error in fucntion get_article_selector")

    # #>


# vim: foldmarker=#<,#>
