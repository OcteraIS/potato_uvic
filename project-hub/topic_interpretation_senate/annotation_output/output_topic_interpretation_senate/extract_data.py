import jsonlines
import csv


# python project-hub/topic_interpretation_senate/annotation_output/output_topic_interpretation_senate/extract_data.py

def extract_slider_values(json_obj):
    label_annotations = json_obj.get("label_annotations", {})
    slider_values = label_annotations.get("slider", {})
    return [slider_values.get(f"S{i}", "") for i in range(1, 15)]

input_jsonl_path = 'project-hub/topic_interpretation_senate/annotation_output/output_topic_interpretation_senate/annotated_instances.jsonl'
output_csv_path = '' # Edit this address to save the output csv file

with jsonlines.open(input_jsonl_path) as jsonl_file, open(output_csv_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header
    header = ['instance_id', 'user', 'displayed_text',\
        'label_annotations.I have read and understood the instructions.<br>',\
        'label_annotations.I want to participate in this research and continue with the study.<br>',\
        'label_annotations.I want to participate in this research and continue with the study.']\
        + [f'label_annotations.slider.s{i}' for i in range(1, 15)]\
        + ['label_annotations.Topic_label', 'label_annotations.Topic_Rationale', 'span_annotations', 'behavioral_data.time_string']
    csv_writer.writerow(header)

    try:
        for obj in jsonl_file:
            # Extract values for each field
            row_values = [
                obj.get('instance_id', ''),
                obj.get('user', ''),
                obj.get('displayed_text', ''),
                obj.get('label_annotations', {}).get('I have read and understood the instructions.<br>', ''),
                obj.get('label_annotations', {}).get('I want to participate in this research and continue with the study.<br>', ''),
                obj.get('label_annotations', {}).get('I want to participate in this research and continue with the study.', ''),
            ] + extract_slider_values(obj) + [
                obj.get('label_annotations', {}).get('Topic_label', ''),
                obj.get('label_annotations', {}).get('Topic_Rationale', ''),
                obj.get('span_annotations', ''),
                obj.get('behavioral_data', {}).get('time_string', ''),
            ]

            # Write the row to the CSV file
            csv_writer.writerow(row_values)
    except StopIteration:
        print("Empty JSON Lines file.")