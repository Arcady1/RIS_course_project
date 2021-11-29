# Стандартные пакеты
import os

# Модули проекта
from database.database import work_with_db
from database.sql_provider import SQLProvider

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


def get_details_info_from_waybill(waybill_id):
    """
    Функция выдает подробное описание товаров в накладной клиента

    Args:
        waybill_id: int. ID накладной, строки которой содержат необходимую информацию о покупке
    Returns:
        List[List[Dict]]. Информация о заказанных деталях для каждой накладной
    """
    sql = provider.get('full_waybill_info.sql', waybill_id=waybill_id)
    return work_with_db(sql)
