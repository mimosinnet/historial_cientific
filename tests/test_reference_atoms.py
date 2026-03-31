import datetime
from unittest.mock import patch, MagicMock
from bibliografia.reference_atoms import Author, Date, JournalDetails, Impact

# Class TestAutor #<
class TestAuthor:

    def test_get_auth_empty_creators(self):
        """Test that an empty creators list returns 'NoAuthor'."""
        author_obj = Author([])
        # Since the default auth_type is 'author', this should hit the empty check
        assert author_obj.get_auth() == "NoAuthor"
        assert author_obj.get_author() == "NoAuthor"
        assert author_obj.get_editor() == "NoAuthor"

    @patch('bibliografia.reference_atoms.neteja', autospec=True)
    @patch('bibliografia.reference_atoms.format_author', autospec=True)
    def test_get_author(self, mock_format_author, mock_neteja):
        """Test getting authors specifically filters out non-authors."""
        # Mocking the common functions
        mock_format_author.side_effect = ["Smith, J.; ", "Doe, J."]
        mock_neteja.return_value = "Smith, J.; Doe, J."

        creators = [
            {"creatorType": "author", "name": "Smith", "firstName": "John", "lastName": "Smith"},
            {"creatorType": "editor", "name": "Editor", "firstName": "Ed", "lastName": "Editor"},
            {"creatorType": "author", "name": "Doe", "firstName": "Jane", "lastName": "Doe"},
        ]

        result = Author(creators).get_author()

        assert result == "Smith, J.; Doe, J."
        assert mock_format_author.call_count == 2
        mock_neteja.assert_called_once_with("Smith, J.; Doe, J.")


    @patch('bibliografia.reference_atoms.neteja', autospec=True)
    @patch('bibliografia.reference_atoms.format_author', autospec=True)
    def test_get_editor(self, mock_format_author, mock_neteja):
        """Test getting editors filters out authors."""
        mock_format_author.return_value = "Editor, E."
        mock_neteja.return_value = "Editor, E."

        creators = [
            {"creatorType": "author", "name": "Smith", "firstName": "John", "lastName": "Smith"},
            {"creatorType": "editor", "name": "Editor", "firstName": "Ed", "lastName": "Editor"},
        ]
        
        result = Author(creators).get_editor()

        assert result == "Editor, E."
        mock_format_author.assert_called_once_with("editor", "Editor", "Ed", "Editor")


    def test_get_auth_1(self) -> None:
        creators = ""
        author = Author(creators).get_auth()
        assert author == "NoAuthor"


    def test_get_auth_2(self) -> None:
        creators = [
            {
                "creatorType": "author",
                "name": "",
                "firstName": "",
                "lastName": "San Román, Beatriz",
            },
            {
                "creatorType": "author",
                "name": "",
                "firstName": "Joan",
                "lastName": "Pujol-Tarres",
            },
            {
                "creatorType": "editor",
                "name": "",
                "firstName": "Joan",
                "lastName": "Pujol-Tarres",
            },
            {
                "creatorType": "author",
                "name": "Montenegro-Martínez, Marisela",
                "firstName": "Marisela",
                "lastName": "Montenegro-Martínez",
            },
        ]
        author = Author(creators).get_auth()
        assert (
            author
            == "San Román, Beatriz; "
            + "Pujol-Tarres, Joan; "
            + "Montenegro-Martínez, Marisela"
        )

# #>

# Class TestDate #<
class TestDate:

    def test_get_year_valid(self):
        """Test year extraction with valid 19xx and 20xx patterns."""
        assert Date("1995-12-01").get_year() == "1995"
        assert Date("Published in 2023").get_year() == "2023"


    def test_get_year_invalid(self):
        """Test year extraction falls back appropriately."""
        assert Date("1899-01-01").get_year() == "No Year"
        assert Date("No date provided").get_year() == "No Year"


    @patch('bibliografia.reference_atoms.get_date_object', autospec=True)
    def test_get_date_valid(self, mock_get_date_object):
        """Test parsing a valid single date."""
        mock_get_date_object.return_value = datetime.datetime(2023, 6, 17)
        assert Date("2023-06-17").get_date() == "17 June 2023"


    @patch('bibliografia.reference_atoms.get_date_object', autospec=True)
    def test_get_date_invalid(self, mock_get_date_object):
        """Test parsing when date object doesn't have strftime (AttributeError)."""
        mock_get_date_object.return_value = "Invalid object" 
        assert Date("Bad Date").get_date() == "NoDate"


    @patch('bibliografia.reference_atoms.get_date_object', autospec=True)
    def test_get_date_range_valid(self, mock_get_date_object):
        """Test formatting a date range."""
        mock_get_date_object.side_effect = [datetime.datetime(2023, 6, 15), datetime.datetime(2023, 6, 20)]
        assert Date("2023-06-15", "2023-06-20").get_date_range() == "15-20 June 2023"


    def test_get_date_range_no_date2(self):
        """Test date range returns empty string if no second date is passed."""
        assert Date("2023-06-15").get_date_range() == ""


    @patch('bibliografia.reference_atoms.get_date_object', autospec=True)
    def test_get_date_range_invalid(self, mock_get_date_object):
        """Test date range ValueError handling."""
        mock_get_date_object.side_effect = ValueError("Invalid format")
        assert Date("2023", "2024").get_date_range() == "NoDate"


    @patch('bibliografia.reference_atoms.get_date_object', autospec=True)
    def test_get_date_range_project_valid(self, mock_get_date_object):
        """Test formatting a project date range."""
        mock_get_date_object.side_effect = [datetime.datetime(2021, 1, 1), datetime.datetime(2023, 12, 31)]
        assert Date("2021", "2023").get_date_range_project() == "From January-2021 to December-2023"


    def test_get_date_range_project_no_date2(self):
        """Test project date range returns empty string if no second date is passed."""
        assert Date("2021-01-01").get_date_range_project() == ""


    @patch('bibliografia.reference_atoms.get_date_object', autospec=True)
    def test_get_date_range_project_invalid(self, mock_get_date_object):
        """Test project date range ValueError handling."""
        mock_get_date_object.side_effect = ValueError("Invalid format")
        assert Date("2021", "2023").get_date_range_project() == "NoDate"

# #>

# Class TestJournalDetails #< 
class TestJournalDetails:

    def test_get_journal_details_all_empty(self):
        """Empty fields should return an empty string."""
        assert JournalDetails("", "", "").get_journal_details() == ""


    def test_get_journal_details_all_present(self):
        """Test correct punctuation when volume, issue, and pages exist."""
        assert JournalDetails("42", "3", "110-125").get_journal_details() == "42(3), 110-125. "


    def test_get_journal_details_no_issue(self):
        """Test formatting without an issue number."""
        assert JournalDetails("42", "", "110-125").get_journal_details() == "42, 110-125. "


    def test_get_journal_details_no_volume(self):
        """Test formatting without a volume number."""
        assert JournalDetails("", "3", "110-125").get_journal_details() == "3, 110-125. "


    def test_get_journal_details_no_pages(self):
        """Test formatting without pages."""
        assert JournalDetails("42", "3", "").get_journal_details() == "42(3). "

# #>

# class TestImpact #<
class TestImpact:

    @patch('bibliografia.reference_atoms.neteja', autospec=True)
    def test_get_impact_all_present(self, mock_neteja):
        """Test formatting of impact factors with JIF, JRC, and SJR."""
        # Have neteja act as a simple strip function for testing
        mock_neteja.side_effect = lambda x: x.strip()
        impact = Impact(jif="4.5", q_jrc="Q1", sjr="1.2", citations="150")
        assert impact.get_impact() == "JCR: 4.5: Q1, 1.2"


    @patch('bibliografia.reference_atoms.neteja', autospec=True)
    def test_get_impact_no_jif(self, mock_neteja):
        """Test formatting when JIF is missing but SJR is present."""
        mock_neteja.side_effect = lambda x: x.strip()
        impact = Impact(jif="", q_jrc="", sjr="1.2", citations="150")
        assert impact.get_impact() == "1.2"


    @patch('bibliografia.reference_atoms.neteja', autospec=True)
    def test_get_impact_no_sjr(self, mock_neteja):
        """Test formatting when SJR is missing."""
        mock_neteja.side_effect = lambda x: x.strip()
        impact = Impact(jif="4.5", q_jrc="Q1", sjr="", citations="150")
        # Trailing comma is expected behavior given the current logic
        assert impact.get_impact() == "JCR: 4.5: Q1,"

# vim: foldmarker=#<,#>
