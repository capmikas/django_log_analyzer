import pytest
from LogFileClass import *

report_list = \
    [
        {
            'handler_name_1': {'DEBUG': 1, 'INFO': 1, 'WARNING': 1, 'ERROR': 1, 'CRITICAL': 1},
            'handler_name_2': {'DEBUG': 1, 'INFO': 1, 'WARNING': 1, 'ERROR': 1, 'CRITICAL': 1}
        },
        {
            'handler_name_3': {'DEBUG': 1, 'INFO': 1, 'WARNING': 1, 'ERROR': 1, 'CRITICAL': 1},
            'handler_name_1': {'DEBUG': 1, 'INFO': 1, 'WARNING': 1, 'ERROR': 1, 'CRITICAL': 1}
        },
        {
            'handler_name_2': {'DEBUG': 1, 'INFO': 1, 'WARNING': 1, 'ERROR': 1, 'CRITICAL': 1},
            'handler_name_6': {'DEBUG': 1, 'INFO': 1, 'WARNING': 1, 'ERROR': 1, 'CRITICAL': 1}
        },
    ]

merged_report = \
    {
        'handler_name_1': {'DEBUG': 2, 'INFO': 2, 'WARNING': 2, 'ERROR': 2, 'CRITICAL': 2},
        'handler_name_2': {'DEBUG': 2, 'INFO': 2, 'WARNING': 2, 'ERROR': 2, 'CRITICAL': 2},
        'handler_name_3': {'DEBUG': 1, 'INFO': 1, 'WARNING': 1, 'ERROR': 1, 'CRITICAL': 1},
        'handler_name_6': {'DEBUG': 1, 'INFO': 1, 'WARNING': 1, 'ERROR': 1, 'CRITICAL': 1}
    }


file_read = \
    {
        '/admin/dashboard/': {'DEBUG': 0, 'INFO': 1, 'WARNING': 0, 'ERROR': 1, 'CRITICAL': 0},
        '/api/v1/cart/': {'DEBUG': 0, 'INFO': 1, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0},
        '/api/v1/products/': {'DEBUG': 0, 'INFO': 1, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0},
        '/api/v1/reviews/': {'DEBUG': 0, 'INFO': 2, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0},
        '/api/v1/support/': {'DEBUG': 0, 'INFO': 1, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0},
        '/api/v1/users/': {'DEBUG': 0, 'INFO': 1, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0}
    }

total_result = \
    {
        'DEBUG': 6,
        'INFO': 6,
        'WARNING': 6,
        'ERROR': 6,
        'CRITICAL': 6,
    }


def test_read_log():
    assert LogFile.read_log('app0.log') == file_read


# @pytest.mark.parametrize("report", report_list)
def test_merge_files():
    assert LogFile.merge_files(report_list) == merged_report


def test_get_total():
    assert LogFile.get_total(merged_report) == total_result
