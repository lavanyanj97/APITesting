import sys
import xml.etree.ElementTree as ET

def calculate_pass_percentage(report_path):
    tree = ET.parse(report_path)
    root = tree.getroot()

    total_tests = int(root.attrib['tests'])
    failures = int(root.attrib['failures'])
    errors = int(root.attrib['errors'])
    skipped = int(root.attrib['skipped'])

    passed_tests = total_tests - (failures + errors + skipped)
    pass_percentage = (passed_tests / total_tests) * 100

    print(f"Total Tests: {total_tests}")
    print(f"Passed Tests: {passed_tests}")
    print(f"Pass Percentage: {pass_percentage:.2f}%")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python calculate_pass_percentage.py <path_to_junit_report>")
        sys.exit(1)

    report_path = sys.argv[1]
    calculate_pass_percentage(report_path)
