"""
 Створіть за допомогою класів та продемонструйте свою реалізацію шкільної бібліотеки 
 (включіть фантазію). Наприклад вона може містити класи Person, Teacher, Student, 
 Book, Shelf, Author, Category і.т.д.
"""

"""
 ОПИС:
- усі дані зберігаються у бд;
- є можливість залогуватися та створити нового студента/учня (+ перевірка логіна і пароля 
на відповідність вимогам);
- створено працівника бібліотеки (ЛОГІН/ПАРОЛЬ - worker/worker);
- наявні операції для студента:
    1) можливість взяти нову книгу відповідно до обраної категорії. При взятті дана книга 
    забирається із загальнодоступних у бібліотеці (не може взяти на руки більше 2 книг - 
    якщо намагається взяти 3тю - генерується виключення про необхідність повернути 1ну з тих, що на руках);
    2) перегляд книг, які взяті у бібліотеці (тобто які потрібно повернути);
    3) повернення книги. При поверненні - книга стає загальнодоступною у бібліотеці.
- наявні операції для працівника:
    1) прегляд доступних для видачі книжок за категоріями.
    2) перегляд переліку студентів та книг, які вони повинні повернути.
    3) додавання нових книг у бібліотеку (припускаємо, що всі книги тільки у 1 екземплярі, тому при доданні перевіряємо
    чи ще не існує даної книги у бібліотеці або на руках у студентів).
"""

import sqlite3
import re
from pathlib import Path

parent_dir = Path(__file__).resolve().parent


class StudentNameValidationError(Exception):
    pass


class PasswordValidationError(Exception):
    pass


class MaxAttemptsPassInputError(Exception):
    pass


class InvalidLoginError(Exception):
    pass


class NoBooksAvailableError(Exception):
    pass


class InvalidInputError(Exception):
    pass


class NoStudentsWithBooksError(Exception):
    pass


class HasNoDebtsError(Exception):
    pass


class BookNotFoundError(Exception):
    pass


class BookOwnerError(Exception):
    pass


class TooManyBooksError(Exception):
    pass


class DataBaseManager:

    def __init__(self, database_path=parent_dir / 'my_library.db'):
        self.database_path = database_path
        self.conn = None
        self.cur = None

    def connect_to_database(self):
        try:
            self.conn = sqlite3.connect(self.database_path)
            self.cur = self.conn.cursor()
            return self.conn, self.cur
        except sqlite3.Error as e:
            raise e

    def close_database_connection(self):
        try:
            if self.conn:
                self.conn.close()
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")

    def create_tables(self):
        try:
            self.connect_to_database()
            if self.conn:
                self.cur.executescript('''
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        is_library_worker BOOLEAN NOT NULL
                    );
                                    
                    CREATE TABLE IF NOT EXISTS books (
                        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        category_id INTEGER,
                        FOREIGN KEY (category_id) REFERENCES book_categories(category_id)
                    );

                    CREATE TABLE IF NOT EXISTS book_categories (
                        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category_name TEXT NOT NULL
                    );

                    CREATE TABLE IF NOT EXISTS user_books (
                        user_id INTEGER,
                        book_id INTEGER,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        category_id INTEGER,               
                        FOREIGN KEY (user_id) REFERENCES users(user_id),
                        FOREIGN KEY (book_id) REFERENCES books(book_id),
                        FOREIGN KEY (category_id) REFERENCES book_categories(category_id)
                );                                  
                ''')
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            self.close_database_connection()

    def register_library_worker(self):
        try:
            self.connect_to_database()
            if self.conn:
                self.cur.execute('INSERT INTO users (username, password, is_library_worker) VALUES (?, ?, ?)', ('worker', 'worker', True))
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            self.close_database_connection()

    def insert_books_data(self):
        book_categories = ['Python', 'JavaScript', 'Java', 'C#', 'C++']
        books = {
            "Python": [
                {"author": "Eric Matthes", "title": "Python Crash Course"},
                {"author": "Luciano Ramalho", "title": "Fluent Python: Clear, Concise, and Effective Programming"},
                {"author": "Al Sweigart", "title": "Automate the Boring Stuff with Python"},
                {"author": "Brett Slatkin", "title": "Effective Python: 90 Specific Ways to Write Better Python"},
                {"author": "David Beazley, Brian K. Jones", "title": "Python Cookbook"}
            ],
            "JavaScript": [
                {"author": "Douglas Crockford", "title": "JavaScript: The Good Parts"},
                {"author": "Kyle Simpson", "title": "You Don't Know JS (book series)"},
                {"author": "Marijn Haverbeke", "title": "Eloquent JavaScript"},
                {"author": "David Flanagan", "title": "JavaScript: The Definitive Guide"},
                {"author": "Nicholas C. Zakas", "title": "Maintainable JavaScript"}
            ],
            "Java": [
                {"author": "Joshua Bloch", "title": "Effective Java"},
                {"author": "Kathy Sierra, Bert Bates", "title": "Head First Java"},
                {"author": "Bruce Eckel", "title": "Thinking in Java"},
                {"author": "Cay S. Horstmann, Gary Cornell", "title": "Core Java Volume I - Fundamentals"},
                {"author": "Robert C. Martin", "title": "Clean Code: A Handbook of Agile Software Craftsmanship"}
            ],
            "C#": [
                {"author": "Andrew Troelsen, Philip Japikse", "title": "Pro C# 7: With .NET and .NET Core"},
                {"author": "Jon Skeet", "title": "C# in Depth"},
                {"author": "Herbert Schildt", "title": "C# 8.0: The Complete Reference"},
                {"author": "Jesse Liberty", "title": "Programming C#"},
                {"author": "Scott W. Ambler, Pramod J. Sadalage", "title": "Refactoring Databases: Evolutionary Database Design"}
            ],
            "C++": [
                {"author": "Bjarne Stroustrup", "title": "The C++ Programming Language"},
                {"author": "Scott Meyers", "title": "Effective Modern C++"},
                {"author": "Herb Sutter, Andrei Alexandrescu", "title": "C++ Coding Standards: 101 Rules, Guidelines, and Best Practices"},
                {"author": "Stanley B. Lippman", "title": "C++ Primer"},
                {"author": "Josuttis, David", "title": "The C++ Standard Library: A Tutorial and Reference"}
            ]
        }
        try:
            self.connect_to_database()
            if self.conn:
                for book_category in book_categories:
                    self.cur.execute('INSERT INTO book_categories (category_name) VALUES (?)', (book_category,))
                for category, books in books.items():
                    for book in books:
                        author = book['author']
                        title = book['title']
                        query = """
                            INSERT INTO books (title, author, category_id)
                            SELECT ?, ?, book_categories.category_id
                            FROM book_categories
                            WHERE book_categories.category_name = ?;
                        """
                        self.cur.execute(query, (title, author, category))

                self.conn.commit()
                print("Дані додано успішно.")
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            self.close_database_connection()


class StudentValidation:

    @staticmethod
    def username_input_validation():
        username = input("Введіть ім'я користувача: ")
        username_pattern = r'^[a-zA-Z0-9]{3,50}$'
        if not re.match(username_pattern, username):
            raise StudentNameValidationError("Ім'я має включати лише латинські літери, бути не меншим за 3 символа і не більшим за 50, забороняється використовувати спецсимволи!")
        return username

    @staticmethod
    def password_input_validation():
        max_attempts = 3
        pass_attempt = 0

        while pass_attempt < max_attempts:
            password = input("Введіть пароль: ")
            password_pattern = r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%&*?])[\dA-Za-z!@#$%&*?]{8,}$'

            try:
                if not re.match(password_pattern, password):
                    raise PasswordValidationError("Пароль повинен бути довжиною мінімум 8 символів,мати хоча б одну цифру, одну велику літеру, одну маленьку та один спецсимвол!")
                else:
                    return password
            except PasswordValidationError as error:
                print(error)

            pass_attempt += 1
            pass_attempts_left = max_attempts - pass_attempt
            if pass_attempts_left > 0:
                print(f"Введено не правильний пароль, залишилось спроб: {pass_attempts_left}")
        if pass_attempt == max_attempts:
            raise MaxAttemptsPassInputError("Досягнуто максимальну кількість спроб для введення паролю")


class UserManager(DataBaseManager, StudentValidation):

    def __init__(self):
        super().__init__()

    def check_user_exists(self, username):
        try:
            self.connect_to_database()
            if self.conn:
                check_username = self.cur.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
                if check_username and check_username[1] == username:
                    return True
                return False
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            self.close_database_connection()

    def register_new_user(self):
        while True:
            try:
                username = self.username_input_validation()

                if self.check_user_exists(username):
                    print("Користувач з даним ім'ям вже існує, придумайте нове ім'я")
                    continue

                password = self.password_input_validation()
                try:
                    self.connect_to_database()
                    if self.conn:
                        self.cur.execute('INSERT INTO users (username, password, is_library_worker) VALUES (?, ?, ?)', (username, password, False))
                        self.conn.commit()
                except sqlite3.Error as e:
                    print(f"Помилка при роботі з SQLite: {e}")
                finally:
                    self.close_database_connection()

                print("Дані успішно додані. Тепер ви можете увійти")
                return username

            except (StudentNameValidationError, PasswordValidationError, MaxAttemptsPassInputError) as error:
                print(error)

    def register_and_login_user(self):
        user_manager_instance = UserManager()
        library_operations_instance = LibraryStudentOperations(user_manager_instance)

        while True:
            current_user = self.register_new_user()
            if current_user:
                print("Бажаєте увійти? (1 - так / 0 - ні): ")
                choice = input()
                if choice == '1':
                    library_operations_instance.library_student_operations(current_user)
                    break
                elif choice == '0':
                    print(f"До наступної зустрічі!")
                    break
                else:
                    print("Ви зробили неправильний вибір, повторіть операцію")

    def login_user(self):
        while True:
            try:
                username = input("Введіть ім'я користувача: ")
                password = input("Введіть пароль: ")
                self.connect_to_database()
                if self.conn:
                    user = self.cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
                    if user:
                        print("Успішний вхід")
                        return username
                    else:
                        raise InvalidLoginError("Введений неправильний логін або пароль, повторіть спробу")

            except (StudentNameValidationError, MaxAttemptsPassInputError, InvalidLoginError) as error:
                print(error)
            except sqlite3.Error as e:
                print(f"Помилка при роботі з SQLite: {e}")
            finally:
                self.close_database_connection()


class LibraryOperations:

    def __init__(self, user_manager):
        self.user_manager = user_manager

    def exit_operation(self):
        print(f"До наступної зустрічі!")

    @staticmethod
    def ask_user_to_continue(message):
        while True:
            user_input = input(message)
            if user_input == '1':
                return True
            elif user_input == '0':
                return False
            else:
                print("Невірна відповідь. Спробуйте ще раз.")

    def view_available_books_by_categories(self):
        try:
            self.user_manager.connect_to_database()
            if self.user_manager.conn:

                categories = self.user_manager.cur.execute('SELECT category_name FROM book_categories').fetchall()
                print("Доступні категорії:")
                for num, category in enumerate(categories, 1):
                    print(f"{num}. {category[0]}")

                choice = input("Оберіть номер категорії: ")

                selected_category_name = categories[int(choice) - 1][0]

                query = '''
                    SELECT title, author
                    FROM books
                    JOIN book_categories ON books.category_id = book_categories.category_id
                    WHERE category_name = ?
                '''
                books = self.user_manager.cur.execute(query, (
                selected_category_name,)).fetchall()
                if not books:
                    raise NoBooksAvailableError("У бібліотеці немає доступних книг")
                else:
                    for num, book in enumerate(books, 1):
                        print(f"{num}. Назва: {book[0]}, Автор: {book[1]}")

        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        except (ValueError, IndexError):
            print("Некоректний вибір. Будь ласка, введіть правильний номер категорії.")
        except NoBooksAvailableError as e:
            print(e)
        finally:
            self.user_manager.close_database_connection()

    def start(self):
        while True:
            try:
                print("Оберіть цифру із запропонованих для вибору необхідних дій: ")
                print("1. Увійти")
                print("2. Зареєструватися")
                print("3. Вихід")

                choice = input("Ваший вибір: ")
                if choice == '1':
                    current_user = self.user_manager.login_user()
                    if current_user == 'worker':
                        worker_operations = LibraryWorkerOperations(self.user_manager)
                        worker_operations.library_worker_operations()
                    else:
                        student_operations = LibraryStudentOperations(self.user_manager)
                        student_operations.library_student_operations(current_user)
                elif choice == '2':
                    self.user_manager.register_and_login_user()
                elif choice == '3':
                    break
                else:
                    raise InvalidInputError("Ви зробили неправильний вибір, повторіть операцію")
            except InvalidInputError as error:
                print(error)


class LibraryWorkerOperations(LibraryOperations):
    
    def __init__(self, user_manager):
        super().__init__(user_manager)

    def check_students_debts(self):
        try:
            self.user_manager.connect_to_database()
            if self.user_manager.conn:
                query = '''
                    SELECT users.username, user_books.title, user_books.author
                    FROM users
                    JOIN user_books ON users.user_id = user_books.user_id
                '''
                students_data = self.user_manager.cur.execute(query).fetchall()
                if not students_data:
                    raise NoStudentsWithBooksError("Немає студентів з книгами на руках.")
                else:
                    print("Студенти з книгами на руках:")
                    for username, book_title, book_author in students_data:
                        print(f"\nСтудент: {username}")
                        print(f" - Книга: {book_title}, Автор: {book_author}")

        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        except NoStudentsWithBooksError as e:
            print(e)
        finally:
            self.user_manager.close_database_connection()

    def add_category(self, category_name):
        try:
            self.user_manager.connect_to_database()
            if self.user_manager.conn:
                query = "SELECT category_id FROM book_categories WHERE category_name = ?"
                result = self.user_manager.cur.execute(query, (category_name,)).fetchone()
                if result:
                    return result[0]
                else:
                    insert_category_query = "INSERT INTO book_categories (category_name) VALUES (?)"
                    self.user_manager.cur.execute(insert_category_query, (category_name,))
                    self.user_manager.conn.commit()
                    return self.user_manager.cur.lastrowid
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            self.user_manager.close_database_connection()

    def check_existing_book(self, title, author, category_id):
        try:
            self.user_manager.connect_to_database()
            if self.user_manager.conn:
                book_query = "SELECT book_id FROM books WHERE title = ? AND author = ? AND category_id = ?"
                book_result = self.user_manager.cur.execute(book_query, (title, author, category_id)).fetchone()
        
                user_query = """
                    SELECT user_books.book_id
                    FROM user_books
                    JOIN books ON user_books.book_id = books.book_id
                    WHERE books.title = ? AND books.author = ? AND books.category_id = ?
                """
                user_result = self.user_manager.cur.execute(user_query, (title, author, category_id)).fetchone()

                if book_result or user_result:
                    return True
                else:
                    return False
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            self.user_manager.close_database_connection()

    def add_book(self):
        try:
            title = input("Введіть назву книги: ")
            author = input("Введіть автора книги: ")
            category_name = input("Введіть категорію книги: ")
            category_id = self.add_category(category_name)

            if self.check_existing_book(title, author, category_id):
                print("Книга вже існує у бібліотеці.")
            else:
                self.user_manager.connect_to_database()
                if self.user_manager.conn: 
                
                    insert_book_query = "INSERT INTO books (title, author, category_id) VALUES (?, ?, ?)"
                    self.user_manager.cur.execute(insert_book_query, (title, author, category_id))
                    self.user_manager.conn.commit()

                    print(f"Книга {title}, автор {author} успішно додана.")

        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        finally:
            self.user_manager.close_database_connection()
                
    def library_worker_operations(self):
        worker_operations = {
            '1': {'title': 'Переглянути доступні залишки книг по категоріям', 'operation': self.view_available_books_by_categories},
            '2': {'title': 'Переглянути студентів та книжки, які вони повинні повернути', 'operation': self.check_students_debts},
            '3': {'title': 'Додати нову книгу до бібліотеки', 'operation': self.add_book},
            '4': {'title': 'Вихід', 'operation': self.exit_operation}
        }
        while True:
            try:
                print("Оберіть номер операції")
                for key, value in worker_operations.items():
                    print(f"{key}.{value['title']}")

                choice = input("Ваший вибір: ")
                if choice in worker_operations:
                    worker_operations[choice]['operation']()

                    if choice == '4' or not self.ask_user_to_continue("Бажаєте продовжити проводити операції з бібліотекою? (1 - так / 0 - ні): "):
                        break

                    else:
                        raise InvalidInputError("Ви зробили неправильний вибір, повторіть операцію")
            except InvalidInputError as error:
                print(error)


class LibraryStudentOperations(LibraryOperations):
    
    def __init__(self, user_manager):
        super().__init__(user_manager)

    def view_student_debts(self, current_user):
        try:
            self.user_manager.connect_to_database()
            if self.user_manager.conn:
                user_id = self.user_manager.cur.execute('SELECT user_id FROM users WHERE username = ?', (current_user,)).fetchone()[0]

                query = 'SELECT title, author FROM user_books WHERE user_id = ?'

                student_data = self.user_manager.cur.execute(query, (
                user_id,)).fetchall()
                if not student_data:
                    raise HasNoDebtsError("У вас немає боргів!")
                else:
                    print("Ваші борги:")
                    for book_title, book_author in student_data:
                        print(f"- Назва книги: {book_title}, Автор: {book_author}")

        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        except HasNoDebtsError as e:
            print(e)
        finally:
            self.user_manager.close_database_connection()

    def take_book(self, current_user):
        try:
            self.view_available_books_by_categories()
            self.user_manager.connect_to_database()
            if self.user_manager.conn:

                user_id = self.user_manager.cur.execute('SELECT user_id FROM users WHERE username = ?', (current_user,)).fetchone()[0]

                query = "SELECT COUNT(book_id) FROM user_books WHERE user_id = ?"
                current_user_books_count = \
                self.user_manager.cur.execute(query, (user_id,)).fetchone()[0]
                if current_user_books_count >= 2:
                    raise TooManyBooksError("Бібліотека не може видати вам не більше 2 книг одночасно. Щоб отримати нову - поверніть одну з тих, що знаходяться у вас.")

                book_title = input("Введіть назву книги, яку ви хочете взяти: ")

                query = "SELECT book_id, title, author, category_id FROM books WHERE title = ?"
                result = self.user_manager.cur.execute(query, (
                book_title,)).fetchone()

                if result:
                    book_id = result[0]
                    title = result[1]
                    author = result[2]
                    category_id = result[3]
                    insert_book_query = 'INSERT INTO user_books (user_id, book_id, title, author, category_id) VALUES (?, ?, ?, ?, ?)'
                    self.user_manager.cur.execute(insert_book_query, (
                    user_id, book_id, title, author, category_id))

                    delete_book_query = 'DELETE FROM books WHERE book_id = ?'
                    self.user_manager.cur.execute(delete_book_query, (book_id,))
                    self.user_manager.conn.commit()
                else:
                    raise BookNotFoundError("Книга з такою назвою не знайдена")
                print(f"Вітаю, ви отримали книгу: {title}, автор: {author}.")
        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        except (TooManyBooksError, BookNotFoundError) as e:
            print(e)
        finally:
            self.user_manager.close_database_connection()

    def return_book(self, current_user):
        try:
            self.view_student_debts(current_user)
            book_title = input("Введіть назву книги, яку ви хочете повернути: ")
            self.user_manager.connect_to_database()
            if self.user_manager.conn:
                user_id = self.user_manager.cur.execute('SELECT user_id FROM users WHERE username = ?', (current_user,)).fetchone()[0]
                query = "SELECT book_id FROM user_books WHERE user_id = ? and title = ?"
                result = self.user_manager.cur.execute(query, (
                user_id, book_title)).fetchone()
                if result:

                    debt_book_id = result[0]
                    insert_book_query = """
                        INSERT INTO books (title, author, category_id)
                        SELECT title, author, category_id
                        FROM user_books
                        WHERE book_id = ?
                    """
                    self.user_manager.cur.execute(insert_book_query, (debt_book_id,))

                    delete_book_query = "DELETE FROM user_books WHERE user_id = ? AND book_id = ?"
                    self.user_manager.cur.execute(delete_book_query, (user_id, debt_book_id))
                    self.user_manager.conn.commit()
                    print(f"Дякуємо, ви повернули книгу!")

                else:
                    raise BookOwnerError("Дана книга не була взята вами з даної бібліотеки")

        except sqlite3.Error as e:
            print(f"Помилка при роботі з SQLite: {e}")
        except BookOwnerError as e:
            print(e)
        finally:
            self.user_manager.close_database_connection()

    def library_student_operations(self, current_user):
        student_operations = {
            '1': {'title': 'Взяти книгу', 'operation': self.take_book},
            '2': {'title': 'Переглянути книжки, які потрібно повернути', 'operation': self.view_student_debts},
            '3': {'title': 'Повернути книгу', 'operation': self.return_book},
            '4': {'title': 'Вихід', 'operation': self.exit_operation}
        }
        while True:
            try:
                print("Оберіть номер операції")
                for key, value in student_operations.items():
                    print(f"{key}.{value['title']}")

                choice = input("Ваший вибір: ")
                if choice in student_operations:
                    operation = student_operations[choice]['operation']
                    if operation == self.exit_operation:
                        operation()
                    else:
                        operation(current_user)
                    if choice == '4' or not self.ask_user_to_continue("Бажаєте продовжити проводити операції з бібліотекою? (1 - так / 0 - ні): "):
                        break

                else:
                    raise InvalidInputError("Ви зробили неправильний вибір, повторіть операцію")
            except InvalidInputError as error:
                print(error)


if __name__=="__main__":
    user_manager = UserManager()
    library_operations = LibraryOperations(user_manager)
    library_operations.start()