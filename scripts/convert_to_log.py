import os
import pandas as pd
import xml.etree.ElementTree as ET

from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.exporter.xes import exporter as xes_exporter


def csv_to_xes(path):
    name = path.split('\\')[-1].split('.')[0]
    data = pd.read_csv(path)
    data['time:timestamp'] = pd.to_datetime(data['time:timestamp'])
    data['concept:name'] = data['concept:name'].astype(str)

    log = log_converter.apply(
        data, variant=log_converter.Variants.TO_EVENT_LOG)

    file_name = name + '.xes'
    xes_exporter.apply(log, file_name)

    # find and replace attribute tag
    search_text = "xmlns"
    replace_text = "xes." + search_text

    with open(file_name, 'r') as file:
        data = file.read()
        data = data.replace(search_text, replace_text)

    with open(file_name, 'w') as file:
        file.write(data)

    return file_name


def merge_xes(paths: list):
    result_file = 'MRS.xes'
    i = 0
    for k in paths:
        source_name = paths.get(k).split('\\')[-1].split('.')[0]
        tree = ET.parse(paths.get(k))
        root = tree.getroot()

        if i == 0:
            if os.path.exists(result_file):
                os.remove(result_file)
            for event in root.iter('event'):
                ET.SubElement(event, 'string', {
                    'key': 'resource', 'value': source_name})
            tree.write(result_file)
        
        else:
            tree_output = ET.parse(result_file)
            root_output = tree_output.getroot()
            for event in root.iter('event'):
                ET.SubElement(event, 'string', {
                    'key': 'resource', 'value': source_name})
            for (trace, trace_output) in zip(root.iter('trace'), root_output.iter('trace')):
                for ev in trace.iter('event'):
                    trace_output.append(ev)

            tree_output.write(result_file)
        i += 1
        
    return result_file