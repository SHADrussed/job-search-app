from typing import List
from .vacancy import Vacancy

def filter_vacancies(vacancies: List[Vacancy], keywords: List[str]) -> List[Vacancy]:
    """
    Filter vacancies by keywords in description.
    
    Args:
        vacancies: List of vacancies to filter
        keywords: List of keywords to filter by
        
    Returns:
        Filtered list of vacancies
    """
    if not keywords:
        return vacancies
        
    filtered = []
    for vacancy in vacancies:
        if all(keyword.lower() in vacancy.description.lower() for keyword in keywords):
            filtered.append(vacancy)
    return filtered

def get_top_vacancies(vacancies: List[Vacancy], limit: int) -> List[Vacancy]:
    """
    Get top N vacancies by salary.
    
    Args:
        vacancies: List of vacancies to filter
        limit: Non-negative number of top vacancies to return
        
    Returns:
        List of top N vacancies without modifying the input list

    Raises:
        ValueError: If limit is negative
    """
    if limit < 0:
        raise ValueError("Limit must be non-negative")
    return sorted(vacancies, reverse=True)[:limit]

def parse_salary_range(salary_range: str) -> tuple[int, int]:
    """
    Parse salary range string into min and max values.
    
    Args:
        salary_range: String in format "min_salary - max_salary"
        
    Returns:
        Tuple of (min_salary, max_salary)
        
    Raises:
        ValueError: If salary range format is invalid
    """
    if not isinstance(salary_range, str) or " - " not in salary_range:
        raise ValueError("Invalid salary range format. Use format: min_salary - max_salary")
        
    try:
        min_str, max_str = salary_range.split(" - ")
        min_salary = int(min_str.strip())
        max_salary = int(max_str.strip())
        if min_salary < 0 or max_salary < 0:
            raise ValueError("Salary values must be positive")
        if min_salary > max_salary:
            raise ValueError("Minimum salary cannot be greater than maximum salary")
        return min_salary, max_salary
    except (ValueError, AttributeError):
        raise ValueError("Invalid salary range format. Use format: min_salary - max_salary")

def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """
    Filter vacancies by salary range.
    
    Args:
        vacancies: List of vacancies to filter
        salary_range: String in format "min_salary - max_salary"
        
    Returns:
        List of vacancies within salary range
    """
    min_salary, max_salary = parse_salary_range(salary_range)
    
    filtered = []
    for vacancy in vacancies:
        avg_salary = vacancy.get_average_salary()
        if min_salary <= avg_salary <= max_salary:
            filtered.append(vacancy)
    return filtered 