import logging
logging.basicConfig(level=logging.DEBUG)

# employee_skills = get_employee_skills()


# --------------------------------------------------------------
# create_suitable_employees_list
# --------------------------------------------------------------

# アサイン可能な従業員のリストを作成する
def create_suitable_employees_list(available_employees, assigned_employees):
  """
  この関数は、アサイン可能な従業員のリストを作成して返します。
  アサイン可能な条件はis_suitable_employees関数を参照します。
  """
  # アサイン可能な従業員のリストを初期化
  suitable_employees_list = []

  # アサイン可能な従業員リストに適切な従業員を追加していく
  for employee_id in available_employees:
    if is_suitable_employees(employee_id, available_employees, assigned_employees):
      suitable_employees_list.append((employee_id, 0))
      logging.debug(f'fc: create_suitable_employees_list: suitable_employees_list: {suitable_employees_list}')

  return suitable_employees_list

# アサイン可能な従業員の条件を設定する
def is_suitable_employees(employee_id, available_employees, assigned_employees):
  """
  この関数は、従業員が割り当て可能であるかどうかを判断して、
  条件に一致する従業員のidを返します。

  条件：
  その日の出勤が可能であること
  すでに別のポジションに割り当てられていないこと
  """
  logging.debug(f'fc: is_suitable_employees, employee_id: {employee_id}')
  is_available = employee_id in available_employees
  is_not_assigned = employee_id not in assigned_employees
  return is_available and is_not_assigned


# --------------------------------------------------------------
# create_matching_skills_employees_list
# --------------------------------------------------------------

# 現在のポジションに対するスキルを持っている従業員を抽出する
def create_matching_skills_employees_list(suitable_employees_list, current_position_code3, skills_index, leader_count, employee_skills):
  """
  この関数は、現在のポジションにアサイン可能なスキルを持つ従業員を抽出して、新たなリストを作成します。
  （ここにパラメータと戻り値の説明を追加）
  """
  
  
  # リストを初期化
  matching_skills_employees_list = []

  # リストに適切な従業員を追加していく
  for employee_tuple in suitable_employees_list:
    employee_id = employee_tuple[0]
    logging.debug(f'fc: create_matching_skills_employees_list, employee_id: {employee_id}')

    skill = employee_skills[employee_id]
    logging.debug(f'fc: create_matching_skills_employees_list, skill: {skill}')
    
    # スキルが一致する従業員をリストに追加
    has_position_skill = skill[skills_index] == '1'
    if has_position_skill:
      matching_skills_employees_list.append((employee_id, int(skill[skills_index + 1])))

  # 現在のポジションがリーダポジションの場合の処理
  is_leader_position = current_position_code3[2] == '1'
  if is_leader_position:
    matching_skills_employees_list = create_to_be_assign_leaders_list(matching_skills_employees_list, employee_skills, leader_count, skills_index)
  
  return matching_skills_employees_list

# 次にアサインされるべきリーダーのリストを作成する
def create_to_be_assign_leaders_list(matching_skills_employees_list, employee_skills, leader_count, skills_index):
  """
  この関数は、リーダーポジションの条件に基づいてリストから従業員を抽出します。

  戻り値: list
  """
  # リーダー適正のある従業員だけを入れるリスト
  matching_skills_leaders_list = []
  
  # リーダー適正のある従業員を抽出する
  for employee_id, _ in matching_skills_employees_list:
    skill = employee_skills[employee_id]
    has_leader_skill = skill[0] == '1'
    
    if has_leader_skill:
      matching_skills_leaders_list.append((employee_id, int(skill[skills_index + 1])))
  
  # リーダーのアサイン回数が最も少ない従業員を抽出する
  to_be_assign_leaders_list = filter_by_min_leader_count(matching_skills_leaders_list, leader_count)
  
  return to_be_assign_leaders_list

# リーダー候補者を、リーダーへのアサイン回数が最も少ない人だけに絞る
def filter_by_min_leader_count(matching_skills_leaders_list, leader_count):
    min_leader_count = min(leader_count[employee[0]] for employee in matching_skills_leaders_list)
    return [employee for employee in matching_skills_leaders_list if leader_count[employee[0]] == min_leader_count]




# --------------------------------------------------------------
# select_best_employee
# --------------------------------------------------------------

# リストの中から、最も適切な従業員を選択する
def select_best_employee(employees_list, total_work_time, current_position_code3, skills_index, positions_details, employee_skills):
  """
  この関数は、suitable_employees_listの中から、最も適切な従業員を選ぶ関数です。
  戻り値: 従業員ID
  """
  logging.debug(f'fc: select_best_employee, skills_index: {skills_index}')
  logging.debug(f'fc: select_best_employee, employees_list: {employees_list}')
  
  
  
  if not employees_list:
    return None
  
  # 勤務時間が最も少ない従業員を抽出
  best_employee_list = filter_by_min_total_work_time(employees_list, total_work_time)
  
  # 勤務時間が同じ従業員がいる、かつ、スキルを参照するポジションである場合、スキル値の低い順に並び替え
  if is_need_more_sort(best_employee_list, current_position_code3, positions_details):
    
    best_employee_list.sort(key=lambda x: int(employee_skills[x[0]][skills_index + 1]))
    logging.debug(f'fc: select_best_employee, best_employee_list: {best_employee_list}')
  
  best_employee = best_employee_list[0][0]
  return best_employee


# 勤務時間が最も少ない従業員だけをリストに残す
def filter_by_min_total_work_time(employees_list, total_work_time):
  """
  この関数は、リスト内の従業員の中から、勤務時間が最少である従業員だけを抽出して、新しいリストを作成する関数です。
  """
  # リスト内で勤務時間が最も少ない値を取得する
  min_total_work_time = min(total_work_time.get(employee[0], 0) for employee in employees_list)
  logging.debug(f'fc: filter_by_min_total_work_time, min_total_wotk_time: {min_total_work_time}')
  
  best_employee_list = [employee for employee in employees_list if total_work_time[employee[0]] == min_total_work_time]
  logging.debug(f'fc: filter_by_min_total_work_time, best_employee_list: {best_employee_list}')
  return best_employee_list

# 更に並び替えが必要な場合の条件設定
def is_need_more_sort(best_employee_list, current_position_code3, positions_details):
  """
  この関数はbest_employee_listに更に並び替えが必要かどうかを判断し、booleanを返します。

  条件：
  """
  # best_employee_list内に複数の従業員がいるか？
  is_not_alone = len(best_employee_list) > 1
  logging.debug(f'fc: is_need_more_sort, is_not_alone:({best_employee_list}, {is_not_alone})')
  
  # 現在割り当てを行っているポジションが、スキルの参照が必要なポジションであるか？
  is_must_have_skills_position = positions_details[current_position_code3[:2]]['must_have_skills'] == True
  logging.debug(f'fc: is_need_more_sort, is_must_have_skills_position:({current_position_code3}, {is_must_have_skills_position})')
  return is_not_alone and is_must_have_skills_position
