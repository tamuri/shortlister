from shortlister.controller import Controller
from pathlib import Path

controller = Controller(path=Path("test-role_0001"))


def test_create_controller():
    result = []
    for applicant in controller.shortlist.applicants:
        result.append(applicant.name)
    expected = ["Emma Jones", "Michael Davis", "Patrick Campbell","Sam Harrington","Sarah Thompson"]

    assert result == expected
