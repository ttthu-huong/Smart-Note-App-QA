# -*- coding: utf-8 -*-
"""
Script rà soát chi tiết số lượng và mapping giữa black_box_test_cases.md và fn23_execution_sheet.md
"""
import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

cases_path = r'D:\Workspace\TBDD\Smart-Note-App-QA\test_cases\black_box\black_box_test_cases.md'
sheet_path = r'D:\Workspace\TBDD\Smart-Note-App-QA\test_cases\execution_sheets\fn23_execution_sheet.md'

print("=== 1. AUDIT TOTAL TEST CASES IN PROJECT ===")
with open(cases_path, 'r', encoding='utf-8') as f:
    cases_text = f.read()

all_tcs = sorted(list(set(re.findall(r'TC-BB-\d+[A-Z]*', cases_text))))
total_project_tcs = len(all_tcs)
print(f"Total Unique TC-IDs across project: {total_project_tcs}")

print("\n=== 2. AUDIT FN-23 TEST CASES IN SPEC ===")
expected_fn23_tcs = [
    'TC-BB-026', 'TC-BB-026B', 'TC-BB-026C', 'TC-BB-026D', 'TC-BB-026E',
    'TC-BB-027', 'TC-BB-027B', 'TC-BB-027C', 'TC-BB-027D', 'TC-BB-027E',
    'TC-BB-027F', 'TC-BB-027G', 'TC-BB-028', 'TC-BB-028B', 'TC-BB-028C',
    'TC-BB-028D', 'TC-BB-029'
]

actual_fn23_tcs = [tc for tc in all_tcs if any(tc == k or tc.startswith(k) for k in expected_fn23_tcs)]
print(f"Expected FN-23 TCs count: {len(expected_fn23_tcs)}")
print(f"Actual FN-23 TCs count in spec: {len(actual_fn23_tcs)}")
print(f"Matched exactly: {expected_fn23_tcs == actual_fn23_tcs}")

print("\n=== 3. AUDIT EXECUTION SHEET (BẢNG 3 & BẢNG 5) ===")
with open(sheet_path, 'r', encoding='utf-8') as f:
    sheet_text = f.read()

lines = sheet_text.splitlines()

# Parse Table 3 (Execution Table)
in_table_3 = False
table_3_rows = []
for line in lines:
    if '## 3. BẢNG THEO DÕI THỰC THI CHI TIẾT' in line:
        in_table_3 = True
        continue
    if in_table_3 and line.startswith('## '):
        in_table_3 = False
        continue
    if in_table_3 and line.startswith('| **TC-BB-'):
        table_3_rows.append(line)

# Parse Table 5 (Evidence Mapping Table)
in_table_5 = False
table_5_rows = []
for line in lines:
    if '## 5. BẢNG EVIDENCE MAPPING' in line:
        in_table_5 = True
        continue
    if in_table_5 and line.startswith('## '):
        in_table_5 = False
        continue
    if in_table_5 and (line.startswith('| **TC-BB-') or line.startswith('| **Exec-')):
        table_5_rows.append(line)

print(f"Table 3 (Execution Rows) count: {len(table_3_rows)}")
print(f"Table 5 (Evidence Rows) count: {len(table_5_rows)}")

print("\n--- TABLE 3 ROWS SUMMARY ---")
table_3_exec_ids = []
for idx, r in enumerate(table_3_rows, 1):
    cols = [c.strip() for c in r.split('|')[1:-1]]
    tc_id = cols[0].replace('*', '')
    exec_id = cols[1].replace('*', '')
    table_3_exec_ids.append(f"{tc_id}-{exec_id}")
    print(f"[{idx:02d}] {tc_id} | {exec_id} | {cols[2][:50]}")

print("\n--- TABLE 5 ROWS SUMMARY ---")
table_5_exec_ids = []
for idx, r in enumerate(table_5_rows, 1):
    cols = [c.strip() for c in r.split('|')[1:-1]]
    exec_id_t5 = cols[0].replace('*', '')
    tc_id_t5 = cols[1].replace('*', '')
    table_5_exec_ids.append(f"{exec_id_t5}")
    print(f"[{idx:02d}] {exec_id_t5} | TC: {tc_id_t5} | {cols[2][:40]}")

print("\n=== VERIFICATION RESULT SUMMARY ===")
print(f"1. Total Project TCs == 118: {total_project_tcs == 118}")
print(f"2. FN-23 Unique TCs == 17: {len(actual_fn23_tcs) == 17}")
print(f"3. Table 3 Execution Rows == 22: {len(table_3_rows) == 22}")
print(f"4. Table 5 Evidence Rows == 22: {len(table_5_rows) == 22}")
