import logging
logging.basicConfig(level=logging.DEBUG)

from ..services.create_single_day_list.create_single_day_list import create_single_day_list



# アサインされたリストをスプレッドシートに書き込む形に並び替える関数
def sort_current_day_dict(positions_data, new_dict, current_game_time):
    
    sorted_new_dict = {}
    for key in sorted(positions_data[current_game_time]['work_code7_list'].keys(), key=int):
        position_code = positions_data[current_game_time]['work_code7_list'][key]
        sorted_new_dict[position_code] = new_dict[position_code]
    return sorted_new_dict



# 試合日ごとのアサインリストを作成する
def create_all_periods_lists(models):
    
    employee_skills = models['employee_skills']
    leader_count = models['work_history']['leader_count'] 
    total_work_time = models['work_history']['total_work_time'] 
    positions_data = models['positions_data']
    work_day_data = models['work_day_data']
    
    logging.info(f'create_all_periods_lists : start!')

    # アサインリストを初期化
    regular_position_dict = {} # 正規ポジションのリスト
    reserve_position_dict = {} # 余剰従業員のリスト

    # game_daysのキー値の数だけ繰り返す
    for current_game_day, game_info in work_day_data['game_days_data'].items():
        # 現在処理を行っている試合日の試合開始時間を取得して、その時間に紐づくポジションデータを取得
        current_game_time = game_info['playballTime']
        positions_count = positions_data[current_game_time]['position_code3_counts']
        
        # 現在処理を行っている対象の試合日について、出勤可能な従業員の情報を取得する
        available_employees = work_day_data['availability_data']['availability'][current_game_day]
        
        logging.info("---------------------------------------------------------------------------------------------------------")
        logging.info(f'current_game_day: {current_game_day}')
        logging.info(f'leader_count: {leader_count}')
        logging.info(f'total_work_time: {total_work_time}')
        logging.debug(f'Playball Time is : {current_game_time}')
        logging.info("---------------------------------------------------------------------------------------------------------")
        
        # 従業員のアサイン処理
        current_assignment_dict, assigned_employees = create_single_day_list(available_employees, positions_count, current_game_time, total_work_time, leader_count, positions_data, employee_skills)
        
        # 従業員の勤務時間を追跡
        for key, value in current_assignment_dict.items():
            if value is None: # 従業員がアサインされてない場合はスキップ
                continue
            work_time = int(key[5]) # キー値の6桁目の値を数値として取得
            total_work_time[value] += work_time
        logging.debug(f"{current_game_day} total_work_time :  {total_work_time}")
        
        # 作成した従業員の辞書をスプシに出力する順番に並び替える
        assigned_dict = sort_current_day_dict(positions_data, current_assignment_dict, current_game_time)
        logging.debug(f' {current_game_day}のアサインリスト:{len(assigned_dict)}人 {assigned_dict}')
        # 割り当てから漏れた従業員を集める
        too_many_employees = [employee for employee in available_employees if employee not in assigned_employees]

        # 結果を各辞書に入れる
        regular_position_dict[current_game_day] = assigned_dict
        reserve_position_dict[current_game_day] = too_many_employees
        
    return regular_position_dict, reserve_position_dict