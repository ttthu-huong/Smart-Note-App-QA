# -*- coding: utf-8 -*-
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

sheet_path = r'D:\Workspace\TBDD\Smart-Note-App-QA\test_cases\execution_sheets\fn23_execution_sheet.md'
cases_path = r'D:\Workspace\TBDD\Smart-Note-App-QA\test_cases\black_box\black_box_test_cases.md'

print("=== FN23 EXECUTION SHEET ===")
if os.path.exists(sheet_path):
    with open(sheet_path, 'r', encoding='utf-8') as f:
        print(f.read())
else:
    print("Sheet file not found!")

print("\n=== BLACK BOX TEST CASES (FN-23 SECTION) ===")
if os.path.exists(cases_path):
    with open(cases_path, 'r', encoding='utf-8') as f:
        text = f.read()
        p = text.find('FN-23')
        if p != -1:
            print(text[p:p+3000])
