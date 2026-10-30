import json
import os
from typing import List, Optional, Dict, Any
from .abstract_storage import AbstractStorage
from ..vacancy import Vacancy

class JSONStorage(AbstractStorage):
    """Implementation of vacancy storage using JSON files."""
    
    def __init__(self, filename: str = "data/vacancies.json") -> None:
        """
        Initialize JSON storage.
        
        Args:
            filename: Path to JSON file for storage
        """
        self.__filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        if not os.path.exists(filename):
            self.__save_vacancies([])
    
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Add a vacancy to storage.
        
        Args:
            vacancy: Vacancy object to store
        """
        vacancies = self.get_vacancies()
        if vacancy not in vacancies:
            vacancies.append(vacancy)
            self.__save_vacancies(vacancies)
    
    def get_vacancies(self, keyword: Optional[str] = None) -> List[Vacancy]:
        """
        Get vacancies from storage, optionally filtered by keyword.
        
        Args:
            keyword: Optional keyword to filter vacancies
            
        Returns:
            List of matching Vacancy objects
        """
        vacancies = self.__load_vacancies()
        if keyword:
            return [v for v in vacancies if keyword.lower() in v.description.lower()]
        return vacancies
    
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Delete a vacancy from storage.
        
        Args:
            vacancy: Vacancy object to delete
        """
        vacancies = self.get_vacancies()
        vacancies = [v for v in vacancies if v != vacancy]
        self.__save_vacancies(vacancies)
    
    def __vacancy_to_dict(self, vacancy: Vacancy) -> Dict[str, Any]:
        """Convert Vacancy object to dictionary."""
        return {
            "title": vacancy.title,
            "url": vacancy.url,
            "salary_from": vacancy.salary_from,
            "salary_to": vacancy.salary_to,
            "currency": vacancy.currency,
            "description": vacancy.description,
            "employer": vacancy.employer
        }
    
    def __dict_to_vacancy(self, data: Dict[str, Any]) -> Vacancy:
        """Convert dictionary to Vacancy object."""
        return Vacancy(
            title=data["title"],
            url=data["url"],
            salary_from=data["salary_from"],
            salary_to=data["salary_to"],
            currency=data["currency"],
            description=data["description"],
            employer=data.get("employer", "Unknown")
        )
    
    def __save_vacancies(self, vacancies: List[Vacancy]) -> None:
        """Save vacancies to JSON file."""
        data = [self.__vacancy_to_dict(v) for v in vacancies]
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def __load_vacancies(self) -> List[Vacancy]:
        """Load vacancies from JSON file."""
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [self.__dict_to_vacancy(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []
