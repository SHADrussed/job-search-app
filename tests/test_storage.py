import pytest
import os
import json
from src.storage.json_storage import JSONStorage
from src.vacancy import Vacancy

@pytest.fixture
def temp_json_file(tmp_path):
    return str(tmp_path / "test_vacancies.json")

@pytest.fixture
def storage(temp_json_file):
    return JSONStorage(temp_json_file)

@pytest.fixture
def sample_vacancy():
    return Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123456",
        salary_from=100000,
        salary_to=150000,
        currency="RUR",
        description="Python, Django"
    )

def test_storage_initialization(temp_json_file):
    storage = JSONStorage(temp_json_file)
    assert os.path.exists(temp_json_file)
    
    with open(temp_json_file, 'r') as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert len(data) == 0

def test_add_vacancy(storage, sample_vacancy):
    storage.add_vacancy(sample_vacancy)
    vacancies = storage.get_vacancies()
    
    assert len(vacancies) == 1
    assert vacancies[0].title == sample_vacancy.title
    assert vacancies[0].url == sample_vacancy.url

def test_add_duplicate_vacancy(storage, sample_vacancy):
    storage.add_vacancy(sample_vacancy)
    storage.add_vacancy(sample_vacancy)  # Try to add the same vacancy
    vacancies = storage.get_vacancies()
    
    assert len(vacancies) == 1  # Should still have only one vacancy

def test_get_vacancies_with_keyword(storage):
    v1 = Vacancy("Python Dev", "url1", 1000, 2000, "RUR", "Python, Django")
    v2 = Vacancy("Java Dev", "url2", 2000, 3000, "RUR", "Java, Spring")
    
    storage.add_vacancy(v1)
    storage.add_vacancy(v2)
    
    python_vacancies = storage.get_vacancies(keyword="Python")
    assert len(python_vacancies) == 1
    assert python_vacancies[0].title == "Python Dev"

def test_delete_vacancy(storage, sample_vacancy):
    storage.add_vacancy(sample_vacancy)
    assert len(storage.get_vacancies()) == 1
    
    storage.delete_vacancy(sample_vacancy)
    assert len(storage.get_vacancies()) == 0

def test_file_persistence(temp_json_file, sample_vacancy):
    # First storage instance
    storage1 = JSONStorage(temp_json_file)
    storage1.add_vacancy(sample_vacancy)
    
    # Second storage instance with same file
    storage2 = JSONStorage(temp_json_file)
    vacancies = storage2.get_vacancies()
    
    assert len(vacancies) == 1
    assert vacancies[0].title == sample_vacancy.title


@pytest.mark.parametrize("employer", ["Example Company", "ООО «Ромашка» 東京"])
def test_employer_persistence(temp_json_file, employer):
    vacancy = Vacancy("Python Dev", "url1", 1000, 2000, "RUR", "Python", employer)
    storage = JSONStorage(temp_json_file)
    storage.add_vacancy(vacancy)

    with open(temp_json_file, encoding="utf-8") as file:
        saved = json.load(file)
    assert saved == [{field: getattr(vacancy, field) for field in Vacancy.__slots__}]

    restored = JSONStorage(temp_json_file).get_vacancies()
    assert len(restored) == 1
    for field in Vacancy.__slots__:
        assert getattr(restored[0], field) == getattr(vacancy, field)


def test_legacy_storage_remains_usable_with_new_records(temp_json_file):
    legacy_record = {
        "title": "Legacy Python Dev",
        "url": "legacy-url",
        "salary_from": 1000,
        "salary_to": 2000,
        "currency": "RUR",
        "description": "Python, Django",
    }
    with open(temp_json_file, "w", encoding="utf-8") as file:
        json.dump([legacy_record], file)

    storage = JSONStorage(temp_json_file)
    legacy_vacancy = storage.get_vacancies()[0]
    assert legacy_vacancy.employer == "Unknown"
    for field, value in legacy_record.items():
        assert getattr(legacy_vacancy, field) == value
    with open(temp_json_file, encoding="utf-8") as file:
        assert json.load(file) == [legacy_record]

    new_vacancy = Vacancy("New Python Dev", "new-url", 2000, 3000, "RUR", "Python", "New Company")
    storage.add_vacancy(new_vacancy)
    storage.add_vacancy(new_vacancy)
    restored = JSONStorage(temp_json_file).get_vacancies(keyword="Python")
    assert [(vacancy.url, vacancy.employer) for vacancy in restored] == [
        ("legacy-url", "Unknown"),
        ("new-url", "New Company"),
    ]

    storage.delete_vacancy(legacy_vacancy)
    remaining = JSONStorage(temp_json_file).get_vacancies()
    assert [(vacancy.url, vacancy.employer) for vacancy in remaining] == [
        ("new-url", "New Company"),
    ]
