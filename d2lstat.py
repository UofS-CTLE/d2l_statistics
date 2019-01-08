#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
d2lstat.py

python d2lstat.py usage_data.csv full_time.csv part_time.csv semester_name number_of_courses_running

Given a correct data set and lists of full- and part-time teachers, this program will generate usage statistics on a
given template, which can be edited under the generate_document function.

Authors:
Dan Ricker <daniel.ricker@scranton.edu>
Sean Batzel <sean.batzel@scranton.edu>

This program is the property of the UofS-CTLE.
"""

import sys
from datetime import date
from typing import List

import weasyprint

DELIMITER = '|'


def filter_for_semester(files_data: List, semester: str) -> List:
    """

    :param files_data:
    :param semester:
    :return:
    """
    final = list()
    for x in files_data:
        y = x.split(DELIMITER)
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
        y = x.split(DELIMITER)
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
        y = x.split(DELIMITER)
        if y[9][-5:] not in seen_crns:
            seen_crns.append(y[9][-5:])
            ret_val.append(x)
    return ret_val


def remove_duplicate_royal(files_data: List) -> List[str]:
    """

    :param files_data:
    :return:
    """
    seen_royal: List[str] = []
    ret_val: List[str] = []
    for x in files_data:
        y = x.split(DELIMITER)
        if y[3] not in seen_royal:
            seen_royal.append(y[3])
            ret_val.append(x)
    return ret_val


def parse_files(usage: str, full_time: str, part_time: str, semester: str, total_courses: int) -> dict:
    """

    :param usage:
    :param full_time:
    :param part_time:
    :param semester:
    :param total_courses:
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
        y = x.split(DELIMITER)
        full_r.append(y[0])
    part_time_file = open(part_time, 'r').readlines()
    for x in part_time_file:
        y = x.split(DELIMITER)
        part_r.append(y[0])
    full = list()
    part = list()
    staff = list()
    for x in range(len(part_r)):
        part_r[x] = part_r[x].strip("\"")
    for x in range(len(full_r)):
        full_r[x] = full_r[x].strip("\"")
    for x in no_dup_r:
        y = x.split(DELIMITER)
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
            'len_full': len(full_time_file),
            'part_time': part,
            'len_part': len(part_time_file),
            'staff': staff,
            'total_courses': total_courses}


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
        x = course.split(DELIMITER)
        if int(x[13]) > 0:
            specifics['assignments'] += 1
        if int(x[15]) > 2:
            specifics['grade'] += 1
        if int(x[16]) > 0:
            specifics['graded'] += 1
        if int(x[18]) > 0:
            specifics['discussion'] += 1
    return {'semester': file_data['semester'],
            'courses_with_usage': len(file_data['semester_no_dup_crn']),
            'faculty_with_usage': len(file_data['semester_no_dup_r']),
            'full_time': len(file_data['full_time']),
            'total_full_time': file_data['len_full'],
            'part_time': len(file_data['part_time']),
            'total_part_time': file_data['len_part'],
            'staff': len(file_data['staff']),
            'specifics': specifics,
            'total_courses': file_data['total_courses']}


def generate_document(stats: dict, semester: str):
    """
    :param stats:
    :param semester:
    :return:
    """
    filename = 'report_' + str(date.today()) + '.html'
    with open('raw_html.html', 'r') as f:
        string = f.read()
    string = string.format(semester,
                           stats['faculty_with_usage'],
                           stats['full_time'],
                           stats['total_full_time'],
                           (stats['full_time'] / stats['total_full_time']) * 100,
                           stats['part_time'],
                           stats['total_part_time'],
                           (stats['part_time'] / stats['total_part_time']) * 100,
                           stats['staff'],
                           stats['courses_with_usage'],
                           stats['total_courses'],
                           (stats['courses_with_usage'] / stats['total_courses']) * 100,
                           stats['specifics']['assignments'],
                           stats['specifics']['grade'],
                           stats['specifics']['graded'],
                           stats['specifics']['discussion'])
    with open(filename, 'w') as f:
        f.write(string)
    pdf = weasyprint.HTML(filename).write_pdf()
    open("report_" + str(date.today()) + ".pdf", 'wb').write(pdf)


def main(usage: str, full_time: str, part_time: str, semester: str, total_courses: int):
    """
    :param usage: The filename of the usage file.
    :param full_time: The filename for the list of full-time faculty.
    :param part_time: The filename fot the list of part-time faculty.
    :param semester: The name of the semester being processed in the format YYYY_Season.
    :param total_courses:
    """
    res = parse_files(usage, full_time, part_time, semester, total_courses)
    res = calculate_stats(res)
    generate_document(res, semester)
    print("Document report generated.")


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(__doc__)
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]))
