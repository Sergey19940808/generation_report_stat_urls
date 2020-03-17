"""
Модуль для генерация файла для тестового прогона приложения
"""


class GeneratorFile:
    def generation_file(self) -> str:
        """
        Генерация тестового файла
        """
        file_name = "test_nodes.txt"
        cnt_nodes = 50000

        urls = [
            "https://app.slack.com/",
            "https://ulearn.me/",
            "https://ru.hexlet.io/",
            "https://mail.google.com/",
            "https://empty.com/"
        ]
        urls_index = 0
        cnt_url_index = len(urls) - 1

        with open(file_name, "w") as f:
            for i in range(cnt_nodes):
                f.write(f"{urls[urls_index]}\n") if i < cnt_nodes - 1 else f.write(f"{urls[urls_index]}")
                next_urls_index = urls_index + 1
                urls_index = next_urls_index if next_urls_index <= cnt_url_index else 0
        return file_name


if __name__ == "__main__":
    generator_file = GeneratorFile()
    generator_file.generation_file()
