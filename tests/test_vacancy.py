import pytest
from src.vacancy import Vacancy

@pytest.fixture
def sample_vacancy():
    return Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123456",
        salary_from=100000,
        salary_to=150000,
        currency="RUR",
        description="Требования: Python, Django, PostgreSQL"
    )

def test_vacancy_creation(sample_vacancy):
    assert sample_vacancy.title == "Python Developer"
    assert sample_vacancy.url == "https://hh.ru/vacancy/123456"
    assert sample_vacancy.salary_from == 100000
    assert sample_vacancy.salary_to == 150000
    assert sample_vacancy.currency == "RUR"
    assert sample_vacancy.description == "Требования: Python, Django, PostgreSQL"

def test_vacancy_validation():
    with pytest.raises(ValueError):
        Vacancy("", "", None, None, "", "")  # Empty strings
    
    with pytest.raises(ValueError):
        Vacancy("Title", "url", -1000, 2000, "RUR", "desc")  # Negative salary
    
    with pytest.raises(ValueError):
        Vacancy("Title", "url", "not_a_number", 2000, "RUR", "desc")  # Invalid salary type

def test_vacancy_comparison():
    v1 = Vacancy("Job1", "url1", 1000, 2000, "RUR", "desc1")
    v2 = Vacancy("Job2", "url2", 2000, 3000, "RUR", "desc2")
    v3 = Vacancy("Job3", "url1", 1000, 2000, "RUR", "desc3")  # Same URL as v1
    
    assert v1 < v2  # Compare by average salary
    assert v2 > v1
    assert v1 == v3  # Compare by URL
    assert v1 != v2

def test_get_average_salary():
    v1 = Vacancy("Job1", "url1", 1000, 2000, "RUR", "desc1")
    v2 = Vacancy("Job2", "url2", None, 2000, "RUR", "desc2")
    v3 = Vacancy("Job3", "url3", 1000, None, "RUR", "desc3")
    v4 = Vacancy("Job4", "url4", None, None, "RUR", "desc4")
    
    assert v1.get_average_salary() == 1500
    assert v2.get_average_salary() == 2000
    assert v3.get_average_salary() == 1000
    assert v4.get_average_salary() == 0

def test_cast_to_object_list():
    data = [
        {
            "name": "Python Developer",
            "alternate_url": "https://hh.ru/vacancy/123456",
            "salary": {
                "from": 100000,
                "to": 150000,
                "currency": "RUR"
            },
            "snippet": {
                "requirement": "Python, Django"
            }
        }
    ]
    
    vacancies = Vacancy.cast_to_object_list(data)
    assert len(vacancies) == 1
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].title == "Python Developer"
    assert vacancies[0].salary_from == 100000 