import os
import math
import time
import logging
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
from robot.api import ExecutionResult
from .keyword_results import KeywordResults
from .html_helper import get_html_content

IGNORE_LIBRARIES = ['BuiltIn', 'Collections', 'DateTime', 'Dialogs', 'OperatingSystem', 'Process', 'SeleniumLibrary', 'String', 'Screenshot', 'Telnet', 'XML']
IGNORE_TYPES = ['FOR ITERATION', 'FOR']

def generate_report(opts):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.info("Converting .xml to .html file. This may take few minutes...")

    # Ignores following library keywords in metrics report
    ignore_library = IGNORE_LIBRARIES
    if opts.ignore:
        ignore_library.extend(opts.ignore)

    # Ignores following type keywords in metrics report
    ignore_type = IGNORE_TYPES
    if opts.ignoretype:
        ignore_type.extend(opts.ignoretype)

    # END OF CUSTOMIZE REPORT
    path = os.path.abspath(os.path.expanduser(opts.path))

    # output.xml files
    output_names = []
    # support "*.xml" of output files
    if ( opts.output == "*.xml" ):
        for item in os.listdir(path): 
            if os.path.isfile(item) and item.endswith('.xml'):
                output_names.append(item)
    else:
        for curr_name in opts.output.split(","):
            curr_path = os.path.join(path, curr_name)
            output_names.append(curr_path)

    # copy the list of output_names onto the one of required_files; the latter may (in the future) 
    # contain files that should not be processed as output_names
    required_files = list(output_names)
    missing_files = [filename for filename in required_files if not os.path.exists(filename)]
    if missing_files:
        # We have files missing.
        exit("output.xml file is missing: {}".format(", ".join(missing_files)))

    mt_time = datetime.now().strftime('%Y%m%d-%H%M%S')

    # Output result file location
    if opts.kwstats_report_name:
        result_file_name = opts.kwstats_report_name
    else:
        result_file_name = 'kwstats-' + mt_time + '.html'
    result_file = os.path.join(path, result_file_name)

    # Read output.xml file
    result = ExecutionResult(*output_names)
    result.configure(stat_config={'suite_stat_level': 2,
                                  'tag_stat_combine': 'tagANDanother'})

    logging.info("1 of 1: Capturing keyword metrics...")
    kwResults = []
    result.visit(KeywordResults(kwResults, ignore_library, ignore_type))

    df = pd.DataFrame(kwResults, columns = ['Keyword Name', 'Status', 'Time'])
    groupedResult = df.groupby(["Keyword Name"], as_index=False, sort=False).agg(' '.join)
    
    rows_html = ''
    for line in groupedResult.to_csv(header=False, sep='\t', index=True).split('\n'):
        if line:
            rows = line.split('\t')
            kwname = rows[1]
            total_count, time_min, time_max, time_avg, time_sum = get_stats(rows[3])
            passed_count = get_pass_percentage(rows[2])
            pass_percentage = round(((passed_count / total_count)*100),2)

            row_content = """
            <tr>
                <td>{kwname}</td>
                <td style="text-align:center">{count}</td>
                <td style="text-align:center">{perc}</td>
                <td style="text-align:center">{min}</td>
                <td style="text-align:center">{max}</td>
                <td style="text-align:center">{avg}</td>
                <td style="text-align:center">{total}</td>
            </tr>
            """.format(kwname=str(kwname), count=str(total_count), perc=str(pass_percentage), min=str(time_min),
             max=str(time_max), avg=str(time_avg), total=str(time_sum) )
            rows_html = str(rows_html) + str(row_content)
    
    report_html = get_html_content(rows_html)
    soup = BeautifulSoup(report_html, "html.parser")
    # Write output as html file
    with open(result_file, 'w') as outfile:
        outfile.write(soup.prettify())

    logging.info("Results file created successfully and can be found at {}".format(result_file))


def get_pass_percentage(value):
    count = 0
    for item in value.split(' '):
        if item == "PASS":
            count += 1
    return count

def get_stats(value):
    list = []
    for item in value.split(' '):
        list.append(float(item))
    
    sum_value = round(sum(list), 2)
    length = len(list)
    average = round(sum_value/length, 2)

    return length, round(min(list),2), round(max(list),2), average, sum_value