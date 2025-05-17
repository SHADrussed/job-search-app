from src import (
    HeadHunterAPI,
    JSONStorage,
    Vacancy,
    filter_vacancies,
    get_top_vacancies,
    get_vacancies_by_salary
)

def user_interaction():
    """Function for user interaction through console."""
    hh_api = HeadHunterAPI()
    storage = JSONStorage()
    
    while True:
        try:
            print("\nВыберите действие:")
            print("1. Поиск вакансий")
            print("2. Показать топ N вакансий по зарплате")
            print("3. Поиск вакансий по ключевым словам")
            print("4. Фильтр по диапазону зарплат")
            print("5. Выход")
            
            choice = input("\nВведите номер действия: ").strip()
            
            if choice == "1":
                query = input("Введите поисковый запрос: ").strip()
                if not query:
                    print("Ошибка: поисковый запрос не может быть пустым")
                    continue
                    
                try:
                    print("Поиск вакансий...")
                    vacancies = hh_api.get_vacancies(query)
                    if not vacancies:
                        print("По вашему запросу ничего не найдено")
                        continue
                    
                    print(f"Найдено {len(vacancies)} вакансий, сохранение данных...")
                    
                    # Store successfully processed vacancies
                    stored_count = 0
                    for vacancy in vacancies:
                        try:
                            storage.add_vacancy(vacancy)
                            stored_count += 1
                        except Exception as e:
                            print(f"Ошибка при сохранении вакансии: {str(e)}")
                            
                    print(f"\nУспешно сохранено {stored_count} вакансий")
                    
                    # Display first 5 vacancies as preview
                    if stored_count > 0:
                        print("\nПример найденных вакансий (первые 5):")
                        for i, vacancy in enumerate(vacancies[:5], 1):
                            print(f"\n{i}. {vacancy}")
                    
                except ValueError as e:
                    print(f"Ошибка валидации данных: {str(e)}")
                except Exception as e:
                    print(f"Ошибка при поиске вакансий: {str(e)}")
                    print("Попробуйте другой поисковый запрос или повторите позже")
            
            elif choice == "2":
                try:
                    n = int(input("Введите количество вакансий для отображения: ").strip())
                    if n <= 0:
                        print("Ошибка: количество должно быть положительным числом")
                        continue
                        
                    vacancies = storage.get_vacancies()
                    if not vacancies:
                        print("\nНет сохраненных вакансий. Сначала выполните поиск вакансий.")
                        continue
                        
                    top_vacancies = get_top_vacancies(vacancies, n)
                    if not top_vacancies:
                        print("\nНет вакансий с указанной зарплатой")
                        continue
                    
                    print(f"\nТоп {n} вакансий по зарплате:")
                    for i, vacancy in enumerate(top_vacancies, 1):
                        print(f"\n{i}. {vacancy}")
                except ValueError:
                    print("Ошибка: введите корректное число")
            
            elif choice == "3":
                keywords = input("Введите ключевые слова через пробел: ").strip().split()
                if not keywords:
                    print("Ошибка: необходимо ввести хотя бы одно ключевое слово")
                    continue
                    
                vacancies = storage.get_vacancies()
                if not vacancies:
                    print("\nНет сохраненных вакансий. Сначала выполните поиск вакансий.")
                    continue
                    
                filtered = filter_vacancies(vacancies, keywords)
                if not filtered:
                    print("\nНет вакансий, соответствующих заданным ключевым словам")
                    continue
                
                print(f"\nНайдено {len(filtered)} вакансий:")
                for i, vacancy in enumerate(filtered, 1):
                    print(f"\n{i}. {vacancy}")
            
            elif choice == "4":
                salary_range = input("Введите диапазон зарплат (формат: min - max): ").strip()
                try:
                    vacancies = storage.get_vacancies()
                    if not vacancies:
                        print("\nНет сохраненных вакансий. Сначала выполните поиск вакансий.")
                        continue
                        
                    filtered = get_vacancies_by_salary(vacancies, salary_range)
                    if not filtered:
                        print("\nНет вакансий в указанном диапазоне зарплат")
                        continue
                    
                    print(f"\nНайдено {len(filtered)} вакансий:")
                    for i, vacancy in enumerate(filtered, 1):
                        print(f"\n{i}. {vacancy}")
                except ValueError as e:
                    print(f"Ошибка: {str(e)}")
            
            elif choice == "5":
                print("До свидания!")
                break
            
            else:
                print("Неверный выбор. Попробуйте снова.")
                
        except KeyboardInterrupt:
            print("\nПрограмма завершена пользователем")
            break
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {str(e)}")
            print("Попробуйте еще раз")

if __name__ == "__main__":
    user_interaction() 