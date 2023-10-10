import pandas as pd
import numpy as np

# 勤務情報シート内でデータ取得に必要な範囲の開始列の列名
start_column_name = "id"

# 勤務情報シートから必要な情報をデータフレームとして取得
def get_df_work_history_data(spreadsheet, sheet_name):
  work_history_master = spreadsheet.worksheet(sheet_name['work_history_master'])
  work_history_data = work_history_master.get_all_values()
  df_work_history_data = pd.DataFrame(work_history_data)
  df_work_history_data.columns = df_work_history_data.iloc[1]
  print(f'df_work_history_data: {df_work_history_data}')
  
  # データ取得範囲の列の設定
  start_column_index = 17 # R列目 "id"列
  
  columns_array = df_work_history_data.columns.get_loc("----")
  print(f'columns_array: {columns_array}')
  
  if isinstance(columns_array, np.ndarray):
    end_column_index = np.where(columns_array)[0][0] - 1
  else:
    end_column_index = columns_array - 1
  print(f'end_column_index: {end_column_index}')

  # データ取得範囲の行の設定
  start_row_index = 2
  end_row_index = np.where(df_work_history_data[start_column_name] == "0")[0][0]
  
  # データ取得範囲を設定  
  df_work_history_data = df_work_history_data.iloc[start_row_index: end_row_index, start_column_index: end_column_index]
  return df_work_history_data

# 従業員ごとに勤務情報を集計する
def create_work_history_dict(spreadsheet, target, sheet_name):
  df_work_history_data = get_df_work_history_data(spreadsheet, sheet_name)
  
  new_dict = {}
  
  # 各行に対しての処理
  for _, row in df_work_history_data.iterrows():
    employee_code = row[start_column_name]
    total = 0  # 従業員の勤務データの合計
    
    # 従業員コード以外の列（勤務データ）に対しての処理
    for work_data in row[1:]:
      # 上からtarget目の文字列を取り出し、数値に変換
      try:
        value = int(work_data[int(target)])
        total += value
      except (ValueError, IndexError):  # 文字列が数値でない、または短すぎる場合の例外処理
        continue
        
    new_dict[employee_code] = total
    
  return new_dict

# 勤務コードのどの桁を取り出すかを設定
leader_count_target = 2
total_work_time_target = 5

# 従業員ごとのリーダーアサイン回数、累積勤務時間の情報を取得する
def get_work_history(spreadsheet, sheet_name):
  leader_count = create_work_history_dict(spreadsheet, leader_count_target, sheet_name)
  total_work_time = create_work_history_dict(spreadsheet, total_work_time_target, sheet_name)
  
  work_history = {
    "leader_count": leader_count,
    "total_work_time": total_work_time,
  }
  
  return work_history

# if __name__ == "__main__":
#   leader_count, total_work_time = get_work_history(spreadsheet)
#   print("leader_count: ", leader_count)
#   print("total_work_time: ", total_work_time)
