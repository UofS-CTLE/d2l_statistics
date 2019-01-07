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
        y = x.split('|')
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
        y = x.split('|')
        if int(y[13]) > 0 or int(y[15]) > 2 or int(y[16]) > 0 or int(y[18]) > 0:
            final.append(x)
    return final


def remove_duplicate_crn(files_data: List) -> List[str]:
    """

    :param files_data:
    :return:
    """
    seen_crns: List[str] = []
    ret_val: List[str] = []
    for x in files_data:
        y = x.split('|')
        if y[9][-5:] not in seen_crns:
            seen_crns.append(y[9][-5:])
            ret_val.append(x)
    for x in files_data:
        y = x.split('|')
        print(y[9][-5:])
    print("Number of unique CRNs {}".format(len(files_data)))
    return ret_val


def remove_duplicate_royal(files_data: List) -> List[str]:
    """

    :param files_data:
    :return:
    """
    seen_royal: List[str] = []
    ret_val: List[str] = []
    for x in files_data:
        y = x.split('|')
        if y[3] not in seen_royal:
            seen_royal.append(x)
            ret_val.append(x)
    return ret_val


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
        y = x.split('|')
        full_r.append(y[0])
    part_time_file = open(part_time, 'r').readlines()
    for x in part_time_file:
        y = x.split('|')
        part_r.append(y[0])
    full = list()
    part = list()
    staff = list()
    for x in range(len(part_r)):
        part_r[x] = part_r[x].strip("\"")
    for x in range(len(full_r)):
        full_r[x] = full_r[x].strip("\"")
    for x in no_dup_r:
        y = x.split('|')
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

    :param file_data: The data produced by the parse function.
    :return: The statistics data required for the report generator.
    """
    specifics = {
            'assignments': 0,
            'grade': 0,
            'graded': 0,
            'discussion': 0
            }
    for course in file_data['semester_no_dup_crn']:
        x = course.split('|')
        if int(x[13]) <= 0: specifics['assignments'] += 1
        if int(x[15]) <= 2: specifics['grade'] += 1
        if int(x[16]) <= 0: specifics['graded'] += 1
        if int(x[18]) <= 0: specifics['discussion'] += 1
    return {'courses_with_usage': len(file_data['semester_no_dup_crn']),
            'faculty_with_usage': len(file_data['semester_no_dup_r']),
            'full_time': len(file_data['full_time']),
            'part_time': len(file_data['part_time']),
            'staff': len(file_data['staff']),
            'specifics': specifics}


def generate_document(stats: dict) -> dict:
    """

    :param stats:
    :return:
    """
    print('Courses with usage: {}'.format(stats['courses_with_usage']))
    print('Faculty with usage: {}'.format(stats['faculty_with_usage']))
    print('Full-time with usage: {}'.format(stats['full_time']))
    print('Part-time: {}'.format(stats['part_time']))
    print('Staff: {}'.format(stats['staff']))
    print('Courses with Assignments: {}'.format(stats['specifics']['assignments']))
    print('Courses with Grade Items: {}'.format(stats['specifics']['grade']))
    print('Courses with Graded Grade Items: {}'.format(stats['specifics']['graded']))
    print('Courses with Discussion Posts: {}'.format(stats['specifics']['discussion']))
    


def main(usage: str, full_time: str, part_time: str, semester: str):
    """

    :param usage: The filename of the usage file.
    :param full_time: The filename for the list of full-time faculty.
    :param part_time: The filename fot the list of part-time faculty.
    :param semester: The name of the semester being processed in the format YYYY_Season.
    """
    res = parse_files(usage, full_time, part_time, semester)
    res = calculate_stats(res)
    generate_document(res)
    print("Document report generated.")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Missing arguments.")
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
