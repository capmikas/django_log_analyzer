import copy
from typing import Dict, List
from collections import defaultdict


class LogFile:

    @classmethod
    def read_log(cls, file_name: str) -> Dict[str, Dict[str, int]]:
        report = defaultdict(lambda: defaultdict(int))
        with open(f"logs/{file_name}", "r") as file:
            for line in file:
                words = line.split()
                handlers = [word for word in words if word.startswith('/')]
                log_level = words[2]
                for handler in handlers:
                    report[handler][log_level] += 1
        return {
            handler: {
                level: counts.get(level, 0)
                for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            }
            for handler, counts in report.items()
        }


    @classmethod
    def merge_files(cls, report_list: List[Dict[str, Dict[str, int]]]) -> Dict[str, Dict[str, int]]:
        merged_report = {}
        log_levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        for report in report_list:
            for handler, stats in report.items():
                if handler not in merged_report:
                    merged_report[handler] = {level: stats[level] for level in log_levels}
                else:
                    for level in log_levels:
                        merged_report[handler][level] += stats[level]
        LogFile.total = LogFile.get_total(merged_report)
        return dict(sorted(merged_report.items()))


    @classmethod
    def print_report(cls, report):
        print(f"HANDLER".ljust(29), f"DEBUG".ljust(10), f"INFO".ljust(10), f"WARNING".ljust(10), f"ERROR".ljust(10),
              f"CRITICAL".ljust(10))
        for handler in report:
            print(f"{handler}".ljust(30),
                  f"{report[handler]['DEBUG']}".ljust(10),
                  f"{report[handler]['INFO']}".ljust(10),
                  f"{report[handler]['WARNING']}".ljust(10),
                  f"{report[handler]['ERROR']}".ljust(10),
                  f"{report[handler]['CRITICAL']}".ljust(10))
        print('________________________________________________________________________________')
        print("...".ljust(30), f"{LogFile.total['DEBUG']}".ljust(10), f"{LogFile.total['INFO']}".ljust(10),
              f"{LogFile.total['WARNING']}".ljust(10), f"{LogFile.total['ERROR']}".ljust(10),
              f"{LogFile.total['CRITICAL']}".ljust(10))

    @classmethod
    def get_total(cls, report: Dict[str, Dict[str, int]]) -> Dict[str, int]:
        total = {level: 0 for level in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')}
        for stats in report.values():
            for level in total:
                total[level] += stats.get(level, 0)
        return total

    @classmethod
    def save_report(cls, report, report_name):
        with open(f"output/{report_name}", "w") as file:
            file.write(f"HANDLER    DEBUG     INFO      WARNING      ERROR\n")
            for handler in report:
                file.write(
                    f"{handler}     {report[handler]['DEBUG']}     {report[handler]['INFO']}     {report[handler]['WARNING']}     {report[handler]['ERROR']}     {report[handler]['CRITICAL']}\n")
            # file.writelines(report)
            file.write('________________________________________________\n')
            file.write(
                f"...     {LogFile.total['DEBUG']}     {LogFile.total['INFO']}     {LogFile.total['WARNING']}     {LogFile.total['ERROR']}     {LogFile.total['DEBUG']}     {LogFile.total['CRITICAL']}\n")
