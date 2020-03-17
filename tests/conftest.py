import os
import pytest

from generation_file import GeneratorFile


@pytest.fixture
def remove_test_file():
    yield
    os.remove("test_urls.txt")


@pytest.fixture
def generator_file():
    return GeneratorFile()
