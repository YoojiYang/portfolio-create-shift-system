import pandas as pd

# スプレッドシートから従業員の出勤可否情報と、今回の処理の対象となる期間を取得
def get_spreadsheet_data(spreadsheet, sheet_name):
  availability_sheet = spreadsheet.worksheet(sheet_name['availability_sheet'])
  target_period_sheet = spreadsheet.worksheet(sheet_name['target_period_sheet'])
  
  availability_data = availability_sheet.get_all_values()
  df_availability = pd.DataFrame(availability_data)

  # アサイン対象期間の情報を取得
  start_day = target_period_sheet.cell(4, 2).value
  end_day = target_period_sheet.cell(4, 4).value
  target_period = {"start_day": start_day, "end_day": end_day}
  
  return df_availability, target_period

# 条件に合致する従業員を辞書にまとめる
def get_employees_by_condition(df, dates, condition):
  employees_by_condition = {}
  for date in dates:
      employees_by_condition[date] = df[df[date] == condition].index.tolist()
  return employees_by_condition

# ３種類の従業員の出勤可否情報を取得する。（1日出勤可能、18時スタート、20時上がり）
def get_employee_availability_data(spreadsheet, sheet_name):
  df_availability, target_period = get_spreadsheet_data(spreadsheet, sheet_name)
  
  # 不要なデータをdfから削除する
  # 行を整える
  header_row = 6
  start_row = 7
  end_row = 99
  
  df_availability.columns = df_availability.iloc[header_row]
  df_availability = df_availability.iloc[start_row: end_row]
  
  # idをキーに設定
  df_availability = df_availability[df_availability['id'].notna() & (df_availability['id'] != '')]
  df_availability.set_index('id', inplace=True)
  
  # 列を整える
  start_day = target_period['start_day']
  end_day = target_period['end_day']
  print('>>>>>>>>>>>>>>>>>>>>>>>>>>  target periods  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
  print(f'fc: get_employee_availability_data, start_day: {start_day}')
  print(f'fc: get_employee_availability_data, end_day: {end_day}')
  print('>>>>>>>>>>>>>>>>>>>>>>>>>>  target periods  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
  
  cols = [col for col in df_availability.columns if start_day <= col <= end_day]
  df_availability = df_availability[cols]
  
  # 辞書の条件を設定
  available_terms = "〇"
  lateStart_terms = "18〜"
  leaveEarly_terms = "〜20"
  
  # work_days_indexの前までのすべての列名を取得
  dates = [col for col in df_availability.columns]

  # 辞書に従業員IDを割り当てる
  availability_employees = get_employees_by_condition(df_availability, dates, available_terms)
  late_start_employees = get_employees_by_condition(df_availability, dates, lateStart_terms)
  leave_early_employees = get_employees_by_condition(df_availability, dates, leaveEarly_terms)
  
  employee_availability_data = {
    "availability": availability_employees,
    "late_start": late_start_employees,
    "leave_early": leave_early_employees,
  }
  
  return employee_availability_data

# 試合日ごとの試合開始時間と必要従業員数を取得
def get_game_days_data(spreadsheet, sheet_name):
  df_game_days, target_period = get_spreadsheet_data(spreadsheet, sheet_name)
  
  # 必要な列と行だけ取り出す
  header_row = 1
  df_game_days.columns = df_game_days.iloc[header_row]
  start_day = target_period['start_day']
  end_day = target_period['end_day']
  target_period_columns = [col for col in df_game_days.columns if start_day <= col <= end_day]
  df_game_days = df_game_days.loc[[3, 4], target_period_columns]
  
  # 必要情報を辞書に格納する
  keys = df_game_days.columns.values
  playballTime_values = df_game_days.iloc[0].values
  potentialAttendance_values = df_game_days.iloc[1].values
  # 辞書に格納
  game_days_data = {}
  for key, playballTime, potentialAttendance in zip(keys, playballTime_values, potentialAttendance_values):
      game_days_data[key] = {
          "playballTime": playballTime,
          "potentialAttendance": potentialAttendance
      }
      
  return game_days_data

# 1つの辞書にまとめる
def get_work_day_data(spreadsheet, sheet_name):
  employee_availability_data = get_employee_availability_data(spreadsheet, sheet_name)
  game_days_data = get_game_days_data(spreadsheet, sheet_name)
  
  work_day_data = {
      'availability_data': employee_availability_data,
      'game_days_data': game_days_data
  }
  
  return work_day_data

# if __name__ == "__main__":
#   work_day_data = get_work_day_data()
#   print(f'availability_data: {work_day_data["availability_data"]}')
#   print(f'game_days_data: {work_day_data["game_days_data"]}')