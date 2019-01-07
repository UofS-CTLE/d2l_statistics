#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

import sys
from typing import List


def filter_for_semester(files_data: List, semester: str) -> List:
    """

    :param files_data:
    :param semester:
    :return:
    """
    final = list()
    for x in files_data:
        y = x.split(',')
        if semester in y[9]:
            final.append(x)
    return final


def get_rows_with_usage(files_data: List) -> List:
    """

    :param files_data:
    :return:
    """
    final = list()
    for x in files_data:
        y = x.split(',')
        if not (int(y[13]) <= 0 or int(y[15]) <= 2 or int(y[16]) <= 0 or int(y[18]) <= 0):
            final.append(x)
    return final


def remove_duplicate_crn(files_data: List) -> List[str]:
    """

    :param files_data:
    :return:
    """
    seen_crns: List[str] = []
    for x in files_data:
        y = x.split(',')
        if y[9][5:] not in seen_crns:
            seen_crns.append(y[9][5:])
        elif y[9][5:] in seen_crns:
            files_data.remove(x)
    return files_data


def remove_duplicate_royal(files_data: List) -> List[str]:
    """

    :param files_data:
    :return:
    """
    seen_royal: List[str] = []
    for x in files_data:
        y = x.split(',')
        if y[3] not in seen_royal:
            seen_royal.append(x)
        elif y[3] in seen_royal:
            files_data.remove(x)
    return files_data


def parse_files(usage: str, full_time: str, part_time: str, semester: str) -> dict:
    """

    :param usage:
    :param full_time:
    :param part_time:
    :param semester:
    :return:
    """
    one = filter_for_semester(open(usage, 'r').readlines(), semester)
    two = get_rows_with_usage(one)
    usage_file = remove_duplicate_crn(two)
    no_dup_r = remove_duplicate_royal(two)
    full_time_file = open(full_time, 'r').readlines()
    full_r = list()
    part_r = list()
    for x in full_time_file:
        y = x.split(',')
        full_r.append(y[0])
    part_time_file = open(part_time, 'r').readlines()
    for x in part_time_file:
        y = x.split(',')
        part_r.append(y[0])
    full = list()
    part = list()
    staff = list()
    for x in range(len(part_r)):
        part_r[x] = part_r[x].strip("\"")
    for x in range(len(full_r)):
        full_r[x] = full_r[x].strip("\"")
    for x in no_dup_r:
        y = x.split(',')
        if y[3] in full_r:
            full.append(y)
        elif y[3] in part_r:
            part.append(y)
        else:
            staff.append(y)
    return {'semester_no_dup_crn': usage_file,
            'semester_no_dup_r': no_dup_r,
            'semester': two,
            'full_time': full,
            'part_time': part,
            'staff': staff}


def calculate_stats(file_data: dict) -> dict:
    """

    :param file_data:
    :return:
    """
    pass


def generate_document(stats: dict) -> dict:
    """

    :param stats:
    :return:
    """
    pass


def main(usage: str, full_time: str, part_time: str, semester: str):
    """

    :param usage: The filename of the usage file.
    :param full_time: The filename for the list of full-time faculty.
    :param part_time: The filename fot the list of part-time faculty.
    :param semester: The name of the semester being processed in the format YYYY_Season.
    """
    parse_files(usage, full_time, part_time, semester)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Missing arguments.")
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
