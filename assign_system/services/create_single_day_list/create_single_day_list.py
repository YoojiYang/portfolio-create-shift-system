import logging
logging.basicConfig(level=logging.DEBUG)

from ...services.create_single_day_list.get_best_employee.get_best_employee import (
    get_best_employee
)

# 次に割り当てを行う対象のポジションを取り出す
def get_target_work_code7_list(positions_data, current_position_code3, current_game_time):
    position_code = [position_code for _, position_code in positions_data[current_game_time]['work_code7_list'].items()
                    if position_code[:3] == current_position_code3
                    ]
    return position_code

# 従業員を条件に従ってアサインする関数
def create_single_day_list(available_employees, positions_count, current_game_time, total_work_time, leader_count, positions_data, employee_skills):
    # この関数が返すリストを初期化
    current_day_dict = {} # ポジションコードをキーとして、値にアサインされた従業員のIDが入る辞書
    assigned_employees = set() # 重複選択を防ぐためのリスト
    
    # 3桁のポジションコードを割り当て順に並び替える（リーダー優先、その後はポジションコードの小さい順）
    sorted_positions_code3 = sorted(positions_count.items(), key=lambda x: (-int(x[0][2]), int(x[0][:2])))

    # 3桁のポジションコードの数だけ以下の処理を繰り返す
    for current_position_code3, original_required_count in sorted_positions_code3:
        # 現在のポジションに必要な従業員数を取得する
        required_count = int(original_required_count)
        
        target_work_code7_list = get_target_work_code7_list(positions_data, current_position_code3, current_game_time) # current_position_code3に一致するポジションコードを取り出す
        
        # ポジションごとの必要な人数の数だけ以下の処理を繰り返す
        for current_target_work_code7 in target_work_code7_list:
            if required_count <= 0: # 必要な従業員数が0になったら次のポジションへ
                break
            best_employee, required_count = get_best_employee(available_employees, assigned_employees, current_position_code3, required_count, total_work_time, leader_count, employee_skills)
            # 最適な従業員を取得できた場合、その従業員を辞書に追加し、割り当て済みのリストに追加する
            if best_employee:
                current_day_dict[current_target_work_code7] = best_employee
                assigned_employees.add(best_employee)
                # アサインするポジションがリーダーの場合、leader_countを+1する
                if current_position_code3[2] == '1':
                    
                    logging.info(f'current_position_code3 : {current_position_code3}')
                    logging.info(f'assigned_leader : {best_employee}')
                    leader_count[best_employee] += 1
                    logging.info(f'leader_count : {leader_count[best_employee]}')

            else:
                current_day_dict[current_target_work_code7] = None

    return current_day_dict, assigned_employees

