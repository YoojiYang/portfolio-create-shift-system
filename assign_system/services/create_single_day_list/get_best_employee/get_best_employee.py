import logging
logging.basicConfig(level=logging.DEBUG)


from ....models.components.positions_details import (
    positions_details,
    must_have_skills_positions,
    
)

from ....services.create_single_day_list.get_best_employee.assign_logic.assign_logic import (
    select_best_employee,
    create_suitable_employees_list,
    create_matching_skills_employees_list,
)

# エラーメッセージをログに出力する
def handle_assignment_error(position_code):
    logging.error(f"Error: Could not assign employee for position_code: {position_code}")


# 指定されたポジションコードに従業員を割り当てて、必要な従業員の数を更新する
def get_best_employee(available_employees, assigned_employees, current_position_code3, required_count, total_work_time, leader_count, employee_skills):
    """
    この関数は、現在のアサイン対象となっているポジションに対して、最適な従業員を選択する関数です。
    """
    # 現在のポジションに対応する、skillsの列数を取得
    skills_index = positions_details[current_position_code3[:2]]['skills_index']
    print('==============================')
    logging.debug(f'fc: get_best_employee, current_position_code3: {current_position_code3}')
    logging.debug(f'fc: get_best_employee, skills_index: {skills_index}')
    logging.debug(f'fc: get_best_employee, assigned_employees: {assigned_employees}')
    print('==============================')
    
    # アサイン可能な従業員のリストを作成
    suitable_employees_list = create_suitable_employees_list(available_employees, assigned_employees)
    
    # 現在割り当てを行っているポジションが、割り当ての条件がないポジションの場合
    if skills_index == None:
        logging.debug(f'fc: get_best_employee, skills index is None')
        best_employee = select_best_employee(suitable_employees_list, total_work_time, current_position_code3, skills_index, positions_details, employee_skills)
        logging.debug(f'fc: get_best_employee, skills index is None: {best_employee}')

    # 現在割り当てを行っているポジションが、割り当ての条件のあるポジションの場合。
    else:
        matching_skills_employees_list = create_matching_skills_employees_list(suitable_employees_list, current_position_code3, skills_index, leader_count, employee_skills)
        best_employee = select_best_employee(matching_skills_employees_list, total_work_time, current_position_code3, skills_index, positions_details, employee_skills)
        logging.debug(f'fc: get_best_employee, main position: {best_employee}')
        
        if not best_employee:
            if current_position_code3[:2] in must_have_skills_positions:
                skills_index = skills_index + 2
                matching_skills_employees_list = create_matching_skills_employees_list(suitable_employees_list, current_position_code3, skills_index, leader_count, employee_skills)
                best_employee = select_best_employee(matching_skills_employees_list, total_work_time, current_position_code3, skills_index, positions_details, employee_skills)
                logging.debug(f'fc: get_best_employee, sub position: {best_employee}')
            else:
                best_employee = select_best_employee(suitable_employees_list, total_work_time, current_position_code3, skills_index, positions_details, employee_skills)
                logging.debug(f'fc: get_best_employee, not in must have skills positions: {best_employee}')
    
    if best_employee:
        required_count -= 1
    else:
        handle_assignment_error(current_position_code3)
        return None, required_count
    return best_employee, required_count
