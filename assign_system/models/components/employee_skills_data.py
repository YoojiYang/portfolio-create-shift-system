import pandas as pd

def get_employee_skills(spreadsheet, sheet_name):
  employee_master = spreadsheet.worksheet(sheet_name['employee_master'])
  employee_data = employee_master.get_all_values()
  df_employee = pd.DataFrame(employee_data)
  df_employee.columns = df_employee.iloc[1]
  df_employee = df_employee.iloc[2:]

  # 辞書を作成
  employee_skills = {row['id']: row['skills'] for index, row in df_employee.iterrows() if row['id']}

  return employee_skills
