class TestGeneratorFile:
    def test_can_generation_file(self, generator_file, remove_test_file):
        """
        Можно сгенерировать файл
        """
        assert generator_file.generation_file() == "test_urls.txt"
