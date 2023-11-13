"""
Написати функцію, яка приймає два параметри: ім'я (шлях) файлу та кількість символів.
Файл також додайте в репозиторій. На екран повинен вивестись список із трьома блоками -
символи з початку, із середини та з кінця файлу. Кількість символів в блоках -
та, яка введена в другому параметрі. Придумайте самі, як обробляти помилку, наприклад,
коли кількість символів більша, ніж є в файлі або, наприклад, файл із двох символів
і треба вивести по одному символу, то що виводити на місці середнього блоку символів?).
Не забудьте додати перевірку чи файл існує.
"""

from pathlib import Path


class FileSizeError(Exception):
    pass


def find_file_blocks(file_name, block_size):
    try:
        file_path = Path(__file__).resolve().parent / file_name

        if not file_path.exists():
            raise FileNotFoundError(f"Файл {file_name} не знайдено")

        with open(file_path, 'r', encoding='utf-8') as file:
            file_data = file.read()

            if block_size > len(file_data):
                raise FileSizeError(
                    "Кількість символів для блоку є більша, ніж є у файлі")

            start_block = file_data[:block_size]
            middle_block = ''
            end_block = ''

            if block_size < len(file_data) <= block_size * 2:
                end_block = file_data[block_size:]

            elif block_size * 2 < len(file_data) < block_size * 3:
                middle_block = file_data[block_size:-block_size]
                end_block = file_data[-block_size:]

            elif len(file_data) >= block_size * 3:
                middle_file_pos = len(file_data) // 2
                mid_block_start = middle_file_pos - block_size // 2
                mid_block_end = mid_block_start + block_size
                middle_block = file_data[mid_block_start:mid_block_end]

                end_block = file_data[-block_size:]

            print([start_block, middle_block, end_block])
    except (FileNotFoundError, FileSizeError) as error:
        print(error)
    except Exception as e:
        print(f"Невідома помилка при роботі з файлом: {e}")


if __name__ == "__main__":
    find_file_blocks('test.txt', 5)

