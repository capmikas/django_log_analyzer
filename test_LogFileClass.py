import random
import pytest
from LogFileClass import *
from collections import defaultdict

log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


@pytest.fixture()
def single_report():
    handlers_names = [random.randint(1, 10) for i in range(random.randint(5, 10))]
    report = {f"handler_name_{name}": {log_level: random.randint(0, 10) for log_level in log_levels} for name in handlers_names}
    return report


@pytest.fixture()
def log_file():
    strings_list = [(f"2025-04-15 12:00:00,000 {random.choice(log_levels)} handler_name_{random.randint(1, 10)} "
                     f"200 OK [192.168.1.59]") for i in range(random.randint(50, 100))]
    return strings_list


def test_parse_log(log_file):
    content_of_log = log_file
    report = defaultdict(lambda: defaultdict(int))
    for line in content_of_log:
        words = line.split()
        handlers = [word for word in words if word.startswith('/')]
        log_level = words[2]
        for handler in handlers:
            report[handler][log_level] += 1
    report_fin =  {
        handler: {
            level: counts.get(level, 0)
            for level in log_levels
        }
        for handler, counts in report.items()
    }
    assert LogFile.parse_log(content_of_log) == report_fin


def test_merge_files(single_report):
    report_list = [single_report for i in range(random.randint(3, 5))]
    merged_report = {}
    for report in report_list:
        for handler, stats in report.items():
            if handler not in merged_report:
                merged_report[handler] = {level: stats[level] for level in log_levels}
            else:
                for level in log_levels:
                    merged_report[handler][level] += stats[level]
    merged_report = dict(sorted(merged_report.items()))
    assert LogFile.merge_files(report_list) == merged_report


def test_get_total(single_report):
    report = single_report
    total = {level: 0 for level in log_levels}
    for stats in report.values():
        for level in total:
            total[level] += stats.get(level, 0)
    assert LogFile.get_total(report) == total
