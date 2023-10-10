from ..models.components.spreadsheet_manager import open_spreadsheet

# スプレッドシートにアサイン結果を書き込む
# 早番と遅番で引数を分ける、　それに付随して書き込み位置なども修正する
def write_to_spreadsheet(regular_position_dict, reserve_position_dict, models):
  # スプレッドシートを開く
  spreadsheet = open_spreadsheet()
  
  work_day_data = models['work_day_data']

  # 各セクションの出力開始と終了のセル位置を指定
  sections = [
      (regular_position_dict, 'C7', 'C36'),
      (reserve_position_dict, 'C40', 'C45'),
      (work_day_data['availability_data']['late_start'], 'C46', 'C51'),
      (work_day_data['availability_data']['leave_early'], 'C52', 'C54'),
  ]

  # 各セクションに対してデータを書き込み
  for section_data, start_cell, end_cell in sections:
    if isinstance(section_data, dict):
      for date, assignments in section_data.items():
        # 出力先のシート名を指定
        worksheet = spreadsheet.worksheet(date)
        if isinstance(assignments, dict):  # 辞書の入れ子構造の場合
          values_to_write = [[value] for value in assignments.values()]
        else:  # 辞書の値がリストの場合
          values_to_write = [[value] for value in assignments]
        worksheet.update(f'{start_cell}:{end_cell}', values_to_write)

  print("All assignments have been written to the Google Spreadsheet")
