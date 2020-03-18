"""
Модуль для генерация отчёта со статистикой по урлам
"""
import sys
import asyncio
import csv
import aiohttp

from typing import Tuple, List
from argparse import ArgumentParser

from aiohttp import ClientSession


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


class Validator:
    @staticmethod
    def check_file_name_unloading_stat(file_name_for_unloading_stat: str):

        if file_name_for_unloading_stat and file_name_for_unloading_stat[-4::1] != ".csv":
            sys.exit(
                Printer.print_msg("Вы ввели неверное название файла для выгрузки, файл должен иметь расширение csv")
            )


class Client:
    def __init__(self):
        pass

    async def ping(self, url: str):
        timeout = aiohttp.ClientTimeout(total=0.007)
        async with ClientSession() as session:
            try:
                async with session.head(url, timeout=timeout) as response:
                    return response.status
            except aiohttp.client.ServerDisconnectedError:
                return "Ошибка недоступности сервера"
            except asyncio.TimeoutError:
                return "Ошибка таймаута"
            except aiohttp.client.ClientConnectorError:
                return "Ошибка подключения"


class GeneratorReportStatUrls:
    def __init__(self):
        arg_parser = ArgParser()
        self.file_name_with_urls = arg_parser.namespace.file_name_with_urls
        self.file_name_for_unloading_stat = arg_parser.namespace.file_name_for_unloading_stat
        self.client = Client()
        self.validator = Validator()

    def get_report(self):
        """
        Получение отчёта
        """
        self.validator.check_file_name_unloading_stat(self.file_name_for_unloading_stat)

        if not self.file_name_for_unloading_stat:
            done_tasks = self._get_done_tasks()
            cnt_state_available, cnt_state_unavailable, cnt_state_not_set = self._get_stat(
                done_tasks
            )
            msg = f"Количество доступных узлов: {cnt_state_available}\n" \
                  f"Количество недоступных узлов: {cnt_state_unavailable}\n" \
                  f"Количество узлов, состояние которых не установлено: {cnt_state_not_set}"
        else:
            done_tasks = self._get_done_tasks()
            cnt_state_available, cnt_state_unavailable, cnt_state_not_set = self._get_stat(
                done_tasks
            )
            self._write_report_csv(
                cnt_state_available,
                cnt_state_unavailable,
                cnt_state_not_set
            )
            msg = f"Отчёт с результатами статистики лежит в файле {self.file_name_for_unloading_stat}"

        return Printer.print_msg(msg)

    def _get_done_tasks(self):
        loop = asyncio.get_event_loop()
        urls = self._get_urls(self.file_name_with_urls)
        chunk_size, pointer = 1000, 0
        done_tasks = []

        tasks = []
        for chunk_urls in range(50):
            for url in urls[pointer:pointer + chunk_size]:
                task = asyncio.ensure_future(
                    self.client.ping(url)
                )
                tasks.append(task)

            features_done, _ = loop.run_until_complete(asyncio.wait(tasks))
            done_tasks.extend([f.result() for f in features_done])
            tasks = []
            pointer += chunk_size
        return done_tasks

    def _get_stat(self, done_tasks: List) -> Tuple[int, int, int]:
        cnt_state_available, cnt_state_unavailable, cnt_state_not_set = 0, 0, 0

        for result in done_tasks:
            if isinstance(result, int):
                if result == 200 or result == 302:
                    cnt_state_available += 1
                else:
                    cnt_state_unavailable += 1
            else:
                if result != "Ошибка таймаута":
                    cnt_state_unavailable += 1
                else:
                    cnt_state_not_set += 1

        return cnt_state_available, cnt_state_unavailable, cnt_state_not_set

    def _write_report_csv(
            self,
            cnt_state_available: int,
            cnt_state_unavailable: int,
            cnt_state_not_set: int
    ):
        data = [
            f"Количество_доступных_узлов, Количество_недоступных_узлов, "
            f"Количество_узлов_состояние_которых_не_установлено".split(","),
            f"{cnt_state_available}, {cnt_state_unavailable}, {cnt_state_not_set}".split(",")

        ]
        with open(self.file_name_for_unloading_stat, "w") as csv_f:
            csv_writer = csv.writer(csv_f, delimiter=',')
            for line in data:
                csv_writer.writerow(line)

    @staticmethod
    def _get_urls(file_name: str):
        with open(file_name, "r") as f:
            urls = f.readlines()
        return urls


if __name__ == "__main__":
    generator_report_stat_nodes = GeneratorReportStatUrls()
    generator_report_stat_nodes.get_report()
