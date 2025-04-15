from typing import Dict, List
from collections import defaultdict


class LogFile:
    log_levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')


    @classmethod
    def read_log(cls, file_name: str) -> List[str]:
        with open(f"logs/{file_name}", "r") as file:
            return file.readlines()


    @classmethod
    def parse_log(cls, log_file: List[str]) -> Dict[str, Dict[str, int]]:
        report = defaultdict(lambda: defaultdict(int))
        for line in log_file:
            words = line.split()
            handlers = [word for word in words if word.startswith('/')]
            log_level = words[2]
            for handler in handlers:
                report[handler][log_level] += 1
        return {
            handler: {
                level: counts.get(level, 0)
                for level in LogFile.log_levels
            }
            for handler, counts in report.items()
        }


    @classmethod
    def merge_files(cls, report_list: List[Dict[str, Dict[str, int]]]) -> Dict[str, Dict[str, int]]:
        merged_report = {}
        for report in report_list:
            for handler, stats in report.items():
                if handler not in merged_report:
                    merged_report[handler] = {level: stats[level] for level in LogFile.log_levels}
                else:
                    for level in LogFile.log_levels:
                        merged_report[handler][level] += stats[level]
        LogFile.total = LogFile.get_total(merged_report)
        return dict(sorted(merged_report.items()))


    @classmethod
    def print_report(cls, report: List[str]):
        print(*report)


    @classmethod
    def get_total(cls, report: Dict[str, Dict[str, int]]) -> Dict[str, int]:
        total = {level: 0 for level in LogFile.log_levels}
        for stats in report.values():
            for level in total:
                total[level] += stats.get(level, 0)
        return total


    @classmethod
    def save_report(cls, report: List[str], report_name: str):
        with open(f"output/{report_name}", "w") as file:
            file.writelines(report)


    @classmethod
    def form_report(cls, report: Dict[str, Dict[str, int]]) -> List[str]:
        formed_report = ['HANDLER'.ljust(29) + "".join([level.ljust(10) for level in LogFile.log_levels]) + '\n']
        for handler in report:
            formed_report.append(f'{handler.ljust(29)}' + "".join([str(report[handler][level]).ljust(10) for level in LogFile.log_levels]) + '\n')
        formed_report.append('_' * 80 + '\n')
        formed_report.append('...'.ljust(29) + "".join([str(LogFile.total[level]).ljust(10) for level in LogFile.log_levels]) + '\n')
        return formed_report