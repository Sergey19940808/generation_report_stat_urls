"""
Модуль для генерация отчёта со статистикой по урлам
"""
from typing import Tuple

import requests

from argparse import ArgumentParser

from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed

from requests_futures.sessions import FuturesSession


class ArgParser:
    def __init__(self):
        arg_parser = ArgumentParser()
        arg_parser.add_argument(
            "file_name_with_urls",
            type=str,
            help="Enter name of file with urls"
        )
        arg_parser.add_argument(
            "--file_name_for_unloading_stat",
            type=str,
            help="Enter name of file for unloading stat",
            default=""
        )
        self.namespace = arg_parser.parse_args()


class Printer:
    @staticmethod
    def print_msg(msg: str):
        print(msg)


class Client:
    def __init__(self):
        self.session = FuturesSession(
            executor=ThreadPoolExecutor(max_workers=100),
        )

    def ping(self, url: str):
        try:
            return self.session.get(url)
        except requests.exceptions.HTTPError:
            return "Ошибка протокола"
        except requests.exceptions.ConnectionError:
            return "Ошибка соединения"
        except requests.exceptions.Timeout:
            return "Ошибка таймаута"
        except requests.exceptions.RequestException:
            return "Ошибка запроса"


class GeneratorReportStatUrls:
    def __init__(self):
        arg_parser = ArgParser()
        self.file_name_with_urls = arg_parser.namespace.file_name_with_urls
        self.file_name_for_unloading_stat = arg_parser.namespace.file_name_for_unloading_stat
        self.client = Client()

    def get_stat(self):
        """
        Получение статистики
        """
        cnt_state_available, cnt_state_unavailable, cnt_state_not_set = self._get_result(self.file_name_with_urls)
        if not self.file_name_for_unloading_stat:
            msg = f"Количество доступных узлов: {cnt_state_available}\n" \
                  f"Количество недоступных узлов: {cnt_state_unavailable}\n" \
                  f"Количество узлов, состояние которых не установлено: {cnt_state_not_set}"

            return Printer.print_msg(msg)
        else:
            pass

    def _get_result(self, file_name: str) -> Tuple[int, int, int]:
        urls = self._get_urls(file_name)[:10000]
        cnt_state_available = 0
        cnt_state_unavailable = 0
        cnt_state_not_set = 0

        for f in as_completed(self.client.ping(url) for url in urls):
            res = f.result()
            if not isinstance(res, type(str)):
                if res.status_code == 200 or res.status_code == 302:
                    cnt_state_available += 1
                else:
                    cnt_state_unavailable += 1
            else:
                if res != "Ошибка таймаута":
                    cnt_state_unavailable += 1
                else:
                    cnt_state_not_set += 1

        return cnt_state_available, cnt_state_unavailable, cnt_state_not_set

    @staticmethod
    def _get_urls(file_name: str):
        with open(file_name, "r") as f:
            urls = f.readlines()
        return urls


if __name__ == "__main__":
    generator_report_stat_nodes = GeneratorReportStatUrls()
    generator_report_stat_nodes.get_stat()

