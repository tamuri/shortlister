import pytest
from shortlister import model
from pathlib import Path

path= Path("test_role")
pickle_file_name = Path("shortlist.pickle")
csv_file=Path("criteria.csv")

def test_load_criteria():
    criteria_result = model.load_criteria(path/csv_file)
    expected = model.Criterion
    for criterion in criteria_result:
        assert type(criterion) is expected
        assert criterion.name and criterion.description and criterion.scores is not None

@pytest.mark.parametrize("folder_path,expected",
                         [(path,["Emma Jones","Michael Davis","Sarah Thompson"]),
                          ("non_existing_folder",[])])
def test_load_applicants(folder_path,expected):
    applicants = model.load_applicants(folder_path)
    result = [applicant.name for applicant in applicants]
    assert result == expected

def test_load_role():
    criteria = [model.Criterion(name="PhD",
                         description="Degree or relevant experience",
                         scores = ("Unsatisfactory","Moderate","Satisfactory","Excellent")),
         model.Criterion(name="Research software",
                         description="Authorship,development and maintenance",
                         scores = ("Unsatisfactory","Moderate","Satisfactory","Excellent")),
         model.Criterion(name="Best practices",
                         description="Issue tracking, testing, documentation etc.",
                         scores = ("Unsatisfactory","Moderate","Satisfactory","Excellent"))]
    
    result = model.load_role(path,model.load_criteria(path/csv_file))
    expected = model.Role(job_title="test_role",
                        job_id="0001",
                        criteria=criteria)

    assert result == expected

def test_save_load():

    s = ("1","2","3","4")
    c = [model.Criterion(name="c1",
                        description="d1",
                        scores = s),
        model.Criterion(name="c2",
                        description="d2",
                        scores = s),
        model.Criterion(name="c3",
                        description="d3",
                        scores = s)]
    
    a = [model.Applicant(name="a1",
                         cv="c1",
                         scores={c[0]:c[0].scores[3],
                                 c[1]:c[1].scores[2],
                                 c[2]:c[2].scores[0]}),
         model.Applicant(name="a2",
                         cv="c2",
                         scores={c[0]: c[0].scores[1],
                                 c[1]: c[1].scores[0]})]

    shortlist = model.Shortlist(role= model.Role(job_title="tests",
                                                job_id="0000",
                                                criteria=c),
                                                applicants=a)
    
    model.save_shortlist(Path("tests"), shortlist)
    result:model.Shortlist = model.load_pickle(Path("tests")/pickle_file_name)

    applicant_criterion_list = [criterion for applicant in result.applicants for criterion in list(applicant.scores.keys())]
    
    for criterion in applicant_criterion_list:
        assert criterion in c
    assert result.role.job_title == "tests"
    assert result.role.job_id == "0000"
    assert result.role.criteria == c
    assert result.applicants == a 
    assert result.applicants[0].name == "a1"
    assert result.applicants[1].name == "a2"
    

    