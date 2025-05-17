# Job Search Application

A Python application for searching job vacancies using the HeadHunter API. This application allows users to search for jobs, filter by salary range, search by keywords, and view top vacancies sorted by salary.

## Features

- Search vacancies using HeadHunter API
- Filter vacancies by salary range
- Keyword-based search
- Sort and display top N vacancies by salary
- Save search results locally
- Command-line interface for easy interaction

## Installation

1. Make sure you have Python 3.9+ and Poetry installed
2. Clone this repository:
   ```bash
   git clone <repository-url>
   cd job-search
   ```
3. Install dependencies:
   ```bash
   poetry install
   ```

## Usage

1. Activate the Poetry environment:
   ```bash
   poetry shell
   ```

2. Run the application:
   ```bash
   python main.py
   ```

### Available Commands

- Search vacancies: Search with keywords and filters
- View saved vacancies: Display previously saved search results
- Filter by salary: Set minimum and maximum salary ranges
- Sort by salary: Display top N vacancies sorted by salary

## Development

### Project Structure

```
job-search/
├── src/
│   ├── api/
│   │   ├── abstract_api.py
│   │   └── hh_api.py
│   ├── storage/
│   │   └── json_storage.py
│   ├── vacancy.py
│   └── utils.py
├── tests/
│   ├── test_utils.py
│   ├── test_storage.py
│   └── test_vacancy.py
└── main.py
```

### Running Tests

```bash
poetry run pytest
```

To view coverage report:
```bash
poetry run pytest --cov-report=html
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure they pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 