from abc import ABC, abstractmethod
from typing import List, Optional
from ..vacancy import Vacancy

class AbstractStorage(ABC):
    """Abstract base class for vacancy storage."""
    
    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Add a vacancy to storage.
        
        Args:
            vacancy: Vacancy object to store
        """
        pass
    
    @abstractmethod
    def get_vacancies(self, keyword: Optional[str] = None) -> List[Vacancy]:
        """
        Get vacancies from storage, optionally filtered by keyword.
        
        Args:
            keyword: Optional keyword to filter vacancies
            
        Returns:
            List of matching Vacancy objects
        """
        pass
    
    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Delete a vacancy from storage.
        
        Args:
            vacancy: Vacancy object to delete
        """
        pass 