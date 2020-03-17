from generation_file import GeneratorFile


class TestGeneratorFile:
    def test_can_generation_file(self):
        """
        Можно сгенерировать файл
        """
        generator_file = GeneratorFile()
        assert generator_file.generation_file() == "test_nodes.txt"
