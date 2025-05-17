from abc import ABC, abstractmethod
from typing import List, Dict, Any

class AbstractAPI(ABC):
    """Abstract base class for job search API interactions."""
    
    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the API."""
        pass
    
    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """
        Get vacancies from the API based on search query.
        
        Args:
            search_query: Search term for vacancies
            
        Returns:
            List of dictionaries containing vacancy data
        """
        pass 