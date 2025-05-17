from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class Vacancy:
    """Class for representing a job vacancy."""
    
    __slots__ = ['title', 'url', 'salary_from', 'salary_to', 'currency', 'description', 'employer']
    
    title: str
    url: str
    salary_from: Optional[int]
    salary_to: Optional[int]
    currency: str
    description: str
    employer: str
    
    def __init__(self, title: str, url: str, salary_from: Optional[int], 
                 salary_to: Optional[int], currency: str, description: str,
                 employer: str = "Unknown") -> None:
        """
        Initialize a Vacancy instance.
        
        Args:
            title: Job title
            url: URL of the vacancy
            salary_from: Lower salary bound
            salary_to: Upper salary bound
            currency: Salary currency
            description: Job description
            employer: Company name
        """
        self.title = self.__validate_string(title, "title")
        self.url = self.__validate_string(url, "url")
        self.salary_from = self.__validate_salary(salary_from, "salary_from")
        self.salary_to = self.__validate_salary(salary_to, "salary_to")
        self.currency = self.__validate_string(currency, "currency")
        self.description = self.__validate_string(description, "description")
        self.employer = self.__validate_string(employer, "employer")
    
    def __validate_string(self, value: str, field: str) -> str:
        """Validate string fields."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Invalid {field}: must be a non-empty string")
        return value.strip()
    
    def __validate_salary(self, value: Optional[int], field: str) -> Optional[int]:
        """Validate salary fields."""
        if value is not None:
            if not isinstance(value, (int, float)) or value < 0:
                raise ValueError(f"Invalid {field}: must be a non-negative number")
            return int(value)
        return None
    
    def __lt__(self, other: 'Vacancy') -> bool:
        """Compare vacancies by average salary."""
        return self.get_average_salary() < other.get_average_salary()
    
    def __eq__(self, other: object) -> bool:
        """Check if vacancies are equal."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.url == other.url
    
    def get_average_salary(self) -> float:
        """Calculate average salary for the vacancy."""
        if self.salary_from is None and self.salary_to is None:
            return 0
        if self.salary_from is None:
            return float(self.salary_to)
        if self.salary_to is None:
            return float(self.salary_from)
        return (self.salary_from + self.salary_to) / 2
    
    def __str__(self) -> str:
        """String representation of the vacancy."""
        salary_info = []
        if self.salary_from is not None:
            salary_info.append(f"от {self.salary_from}")
        if self.salary_to is not None:
            salary_info.append(f"до {self.salary_to}")
        salary_str = " ".join(salary_info) + f" {self.currency}" if salary_info else "Зарплата не указана"
        
        return f"{self.title} ({self.employer})\nЗарплата: {salary_str}\n{self.description}\nПодробнее: {self.url}\n"
    
    @staticmethod
    def cast_to_object_list(vacancies_data: List[Dict[str, Any]]) -> List['Vacancy']:
        """
        Convert list of vacancy dictionaries to list of Vacancy objects.
        
        Args:
            vacancies_data: List of dictionaries with vacancy data from HH API
            
        Returns:
            List of Vacancy objects
        """
        vacancies = []
        for data in vacancies_data:
            try:
                # Extract salary information
                salary_data = data.get("salary", {}) or {}
                
                # Get description combining both requirement and responsibility
                snippet = data.get("snippet", {}) or {}
                description_parts = []
                
                requirement = snippet.get("requirement")
                if requirement:
                    description_parts.append(f"Требования: {requirement}")
                
                responsibility = snippet.get("responsibility")
                if responsibility:
                    description_parts.append(f"Обязанности: {responsibility}")
                
                description = " | ".join(description_parts) if description_parts else "Описание отсутствует"
                
                # Get employer name
                employer_data = data.get("employer", {}) or {}
                employer = str(employer_data.get("name", "Unknown"))
                
                # Create vacancy object
                vacancy = Vacancy(
                    title=str(data.get("name", "Без названия")),
                    url=str(data.get("alternate_url", "https://hh.ru")),
                    salary_from=salary_data.get("from"),
                    salary_to=salary_data.get("to"),
                    currency=str(salary_data.get("currency", "RUR")),
                    description=description,
                    employer=employer
                )
                vacancies.append(vacancy)
            except Exception as e:
                print(f"Warning: Failed to process vacancy: {str(e)}")
                continue
                
        return vacancies 