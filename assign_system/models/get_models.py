from .components.spreadsheet_manager import open_spreadsheet
from .components.employee_skills_data import get_employee_skills
from .components.positions_data import get_positions_data
from .components.work_day_data import get_work_day_data
from .components.work_history_data import get_work_history
from .components.positions_details import positions_details, must_have_skills_positions
from .components.sheet_name import sheet_name

def get_models():
  spreadsheet = open_spreadsheet()
  
  employee_skills = get_employee_skills(spreadsheet, sheet_name)
  positions_data = get_positions_data(spreadsheet, sheet_name)
  work_day_data = get_work_day_data(spreadsheet, sheet_name)
  work_history = get_work_history(spreadsheet, sheet_name)

  models = {
    "employee_skills": employee_skills,
    "positions_data": positions_data,
    "work_day_data": work_day_data,
    "work_history": work_history,
    "positions_details": positions_details,
    "must_have_skills_positions": must_have_skills_positions,
  }
  
  return models

if __name__ == "__main__":
  models = get_models()
  # print(f'employee_skills: {models["employee_skills"]}')

  # print(f'positions_data: {models["positions_data"]}')

  # print(f'work_day_data: {models["work_day_data"]}')

  print(f'work_history: {models["work_history"]}')
  print(f'leader_count: {models["work_history"]["leader_count"]}')
  print(f'total_work_time: {models["work_history"]["total_work_time"]}')

  # print(f'positions_details: {models["positions_details"]}')
  # print(f'must_have_skills_positions: {models["must_have_skills_positions"]}')
