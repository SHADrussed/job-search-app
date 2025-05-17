import pytest
from unittest.mock import patch, MagicMock
from src.api.hh_api import HeadHunterAPI
from src.vacancy import Vacancy

@pytest.fixture
def api():
    return HeadHunterAPI()

@pytest.fixture
def mock_response():
    return {
        "items": [
            {
                "id": "1234",
                "name": "Python Developer",
                "salary": {
                    "from": 100000,
                    "to": 150000,
                    "currency": "RUR"
                },
                "snippet": {
                    "requirement": "Python, Django, REST",
                    "responsibility": "Development of web applications"
                },
                "employer": {
                    "name": "Test Company"
                },
                "alternate_url": "https://hh.ru/vacancy/1234"
            }
        ]
    }

def test_get_vacancies(api, mock_response):
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200
        
        vacancies = api.get_vacancies("python developer")
        
        assert len(vacancies) == 1
        vacancy = vacancies[0]
        assert isinstance(vacancy, Vacancy)
        assert vacancy.title == "Python Developer"
        assert vacancy.salary_from == 100000
        assert vacancy.salary_to == 150000
        assert vacancy.employer == "Test Company"
        assert vacancy.url == "https://hh.ru/vacancy/1234"

def test_get_vacancies_no_salary(api):
    mock_response = {
        "items": [
            {
                "id": "1234",
                "name": "Python Developer",
                "salary": None,
                "snippet": {
                    "requirement": "Python, Django, REST",
                    "responsibility": "Development of web applications"
                },
                "employer": {
                    "name": "Test Company"
                },
                "alternate_url": "https://hh.ru/vacancy/1234"
            }
        ]
    }
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200
        
        vacancies = api.get_vacancies("python developer")
        
        assert len(vacancies) == 1
        vacancy = vacancies[0]
        assert vacancy.salary_from is None
        assert vacancy.salary_to is None

def test_get_vacancies_api_error(api):
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 500
        
        with pytest.raises(Exception) as exc_info:
            api.get_vacancies("python developer")
        
        assert "API request failed" in str(exc_info.value)

def test_get_vacancies_invalid_response(api):
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"invalid": "response"}
        mock_get.return_value.status_code = 200
        
        with pytest.raises(KeyError):
            api.get_vacancies("python developer") 