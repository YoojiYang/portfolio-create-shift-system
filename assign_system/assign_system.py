from .models.get_models import get_models

from .services.create_all_periods_lists import create_all_periods_lists
from .services.write_spreadsheet import write_to_spreadsheet


def assign_system():
    # 必要なデータを取得
    models = get_models()
    
    # 従業員のアサインリストを作成
    regular_position_dict, reserve_position_dict = create_all_periods_lists(models)

    # 作成したアサインリストをスプレッドシートに書き込む
    write_to_spreadsheet(regular_position_dict, reserve_position_dict, models)


if __name__ == "__assign_system__":
    assign_system()