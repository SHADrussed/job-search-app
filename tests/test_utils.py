import pytest
from src.utils import (
    filter_vacancies,
    get_top_vacancies,
    get_vacancies_by_salary,
    parse_salary_range
)
from src.vacancy import Vacancy

@pytest.fixture
def sample_vacancies():
    return [
        Vacancy("Python Dev", "url1", 100000, 150000, "RUR", "Python, Django, PostgreSQL", "Company A"),
        Vacancy("Java Dev", "url2", 150000, 200000, "RUR", "Java, Spring, MySQL", "Company B"),
        Vacancy("Python Senior", "url3", 200000, 250000, "RUR", "Python, AWS, Kubernetes", "Company C")
    ]

def test_filter_vacancies(sample_vacancies):
    # Test with single keyword
    filtered = filter_vacancies(sample_vacancies, ["Python"])
    assert len(filtered) == 2
    assert all("Python" in v.description for v in filtered)
    
    # Test with multiple keywords
    filtered = filter_vacancies(sample_vacancies, ["Python", "AWS"])
    assert len(filtered) == 1
    assert filtered[0].title == "Python Senior"
    
    # Test with no matches
    filtered = filter_vacancies(sample_vacancies, ["Ruby"])
    assert len(filtered) == 0
    
    # Test with empty keywords
    filtered = filter_vacancies(sample_vacancies, [])
    assert len(filtered) == len(sample_vacancies)

def test_get_top_vacancies(sample_vacancies):
    # Test getting top 2
    top = get_top_vacancies(sample_vacancies, 2)
    assert len(top) == 2
    assert top[0].title == "Python Senior"  # Highest salary
    assert top[1].title == "Java Dev"  # Second highest
    
    # Test getting more than available
    top = get_top_vacancies(sample_vacancies, 5)
    assert len(top) == 3
    
    # Test getting none
    top = get_top_vacancies(sample_vacancies, 0)
    assert len(top) == 0

def test_parse_salary_range():
    # Test valid range
    min_salary, max_salary = parse_salary_range("100000 - 200000")
    assert min_salary == 100000
    assert max_salary == 200000
    
    # Test invalid formats
    with pytest.raises(ValueError):
        parse_salary_range("invalid")
    
    with pytest.raises(ValueError):
        parse_salary_range("100000-200000")  # No spaces
    
    with pytest.raises(ValueError):
        parse_salary_range("200000 - 100000")  # Max less than min
    
    with pytest.raises(ValueError):
        parse_salary_range("-100 - 100")  # Negative salary

def test_get_vacancies_by_salary(sample_vacancies):
    # Test valid range
    filtered = get_vacancies_by_salary(sample_vacancies, "120000 - 180000")
    assert len(filtered) == 2
    assert "Python Dev" in [v.title for v in filtered]
    assert "Java Dev" in [v.title for v in filtered]
    
    # Test range with no matches
    filtered = get_vacancies_by_salary(sample_vacancies, "300000 - 400000")
    assert len(filtered) == 0
    
    # Test invalid range
    with pytest.raises(ValueError):
        get_vacancies_by_salary(sample_vacancies, "invalid range") 