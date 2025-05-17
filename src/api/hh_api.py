import requests
from typing import List, Dict, Any
from .abstract_api import AbstractAPI
from ..vacancy import Vacancy

class HeadHunterAPI(AbstractAPI):
    """Implementation of the HeadHunter API client."""
    
    def __init__(self) -> None:
        """Initialize HeadHunter API client."""
        self.__base_url: str = "https://api.hh.ru/vacancies"
        self.__per_page: int = 100
        self.__headers: Dict[str, str] = {
            "User-Agent": "HH-User-Agent"
        }
    
    def connect(self) -> None:
        """Establish connection to the API."""
        # No need to check connection for each request since HH API doesn't require it
        pass
    
    def get_vacancies(self, search_query: str) -> List[Vacancy]:
        """
        Get vacancies from HH API based on search query.
        
        Args:
            search_query: Search term for vacancies
            
        Returns:
            List of Vacancy objects
            
        Raises:
            Exception: If API request fails
            KeyError: If API response is invalid
        """
        params = {
            "text": search_query,
            "per_page": self.__per_page,
            "page": 0,
            "area": 113,  # Russia
            "only_with_salary": True
        }
        
        try:
            response = requests.get(
                self.__base_url,
                headers=self.__headers,
                params=params
            )
            
            if response.status_code != 200:
                raise Exception("API request failed")
            
            data = response.json()
            if "items" not in data:
                raise KeyError("Invalid API response format")
                
            return Vacancy.cast_to_object_list(data["items"])
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except ValueError as e:
            raise Exception(f"Failed to parse API response: {str(e)}") 