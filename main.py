from sys import argv
from multiprocessing import Pool, cpu_count
import LogFileClass
import os.path


def main():
    report_file_name = ''
    words_list = argv[1:]
    file_name_list = []
    for i, word in enumerate(words_list):
        if word == '--report':
            try:
                report_file_name = words_list[i+1]
            except Exception as e:
                exit('Необходимо ввести название файла')
            break
        else:
            if os.path.exists(f"logs/{word}"):
                file_name_list.append(word)
            else:
                print(f"Файла {word} не существует")
    if not file_name_list:
        exit('При вызове программы необходимо ввести названия файлов')
    print(f"\nЛоги для анализа: {file_name_list}\n")
    with Pool(cpu_count()) as pool:
        report_list = pool.map(read_file_pool, file_name_list)
    merged_file = LogFileClass.LogFile.merge_files(report_list)
    report = LogFileClass.LogFile.form_report(merged_file)
    LogFileClass.LogFile.print_report(report)
    if report_file_name:
        LogFileClass.LogFile.save_report(report, report_file_name)


def read_file_pool(file_name):
    log_file = LogFileClass.LogFile.read_log(file_name)
    report = LogFileClass.LogFile.parse_log(log_file)
    return report


if __name__ == '__main__':
    main()
