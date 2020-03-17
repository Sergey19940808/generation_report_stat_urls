"""
Модуль для генерация файла для тестового прогона приложения
"""


class GeneratorFile:
    @staticmethod
    def generation_file() -> str:
        """
        Генерация тестового файла
        """
        file_name = "test_urls.txt"
        cnt_urls = 50000

        urls = [
            "https://app.slack.com/",
            "https://ulearn.me/",
            "https://ru.hexlet.io/",
            "https://mail.google.com/",
        ]
        urls_index = 0
        cnt_url_index = len(urls) - 1

        with open(file_name, "w") as f:
            for i in range(cnt_urls):
                f.write(f"{urls[urls_index]}\n") if i < cnt_urls - 1 else f.write(f"{urls[urls_index]}")
                next_urls_index = urls_index + 1
                urls_index = next_urls_index if next_urls_index <= cnt_url_index else 0
        return file_name


if __name__ == "__main__":
    GeneratorFile.generation_file()
