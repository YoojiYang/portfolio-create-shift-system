positions_count =  {'111': 1, '110': 5, '121': 1, '120': 3, '130': 2, '140': 2, '190': 4, '200': 3, '151': 1, '150': 2, '161': 1, '160': 1, '170': 2, '180': 2}

positions_data =  {'1': '111D181', '2': '110D181', '3': '110D182', '4': '110D183', '5': '110D371', '6': '110D372', '7': '121D181', '8': '120D181', '9': '120D371', '10': '120D372', '11': '130D181', '12': '130D461', '13': '140D181', '14': '140D461', '15': '190D371', '16': '190D372', '17': '190D861', '18': '190D862', '19': '200D371', '20': '200D372', '21': '200D461', '22': '151D181', '23': '150D181', '24': '150D371', '25': '161D181', '26': '160D371', '27': '170D371', '28': '170D372', '29': '180D461', '30': '180D462'}

current_game_time = "13:00"


# 3桁の勤務コードを割り当て順に並び替える（リーダー優先、その後はポジションコードの小さい順）
sorted_positions_code3 = sorted(positions_count.items(), key=lambda x: (-int(x[0][2]), int(x[0][:2])))

print(sorted_positions_code3)


# 次に割り当てを行う対象のポジションを取り出す
def get_position_number2(current_position_code3, current_game_time):
  position_code = [position_code for _, position_code in positions_data.items()
                  if position_code[:3] == current_position_code3
                  ]
  return position_code



# 3桁のポジションコードの数だけ以下の処理を繰り返す
for current_position_code3, original_required_employees in sorted_positions_code3:
  # 現在のポジションに必要な従業員数を取得する
  required_employees = int(original_required_employees)
  
  position_number2 = get_position_number2(current_position_code3, current_game_time) # current_position_code3に一致するポジションコードを取り出す

  print(position_number2)