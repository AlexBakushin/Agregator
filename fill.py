import datetime
import json

import bson


async def main(inp):
    """
    Главная функция бота
    :param inp: json с параметрами запроса
    :return:  json с ответом
    """
    # Преобразование входящих данных
    dt_from_obj = datetime.datetime.strptime(inp["dt_from"], "%Y-%m-%dT%H:%M:%S")
    dt_to_obj = datetime.datetime.strptime(inp["dt_upto"], "%Y-%m-%dT%H:%M:%S")
    # Пустой список для хранения !необходимых! данных
    right_data = []
    # Пустой словарь для ответа
    answer = {"dataset": [], "labels": []}

    #  Открываем файл с готовыми данными
    with open('sample_collection.bson', 'rb') as f:
        data = bson.decode_all(f.read())

        # Фильтруем данные
        for i in data:
            if dt_from_obj <= i["dt"] <= dt_to_obj:
                right_data.append(i)

        # Если валидация для месяца
        if inp["group_type"] == "month":
            val = 0
            for j in range(dt_to_obj.month - dt_from_obj.month + 1):
                for i in right_data:
                    if i["dt"].month == dt_from_obj.month + j:
                        val += i["value"]

                answer["dataset"].append(val)
                val = 0
                answer["labels"].append(
                    f"{datetime.datetime(year=dt_from_obj.year, month=dt_from_obj.month + j, day=1, hour=0).isoformat()}")

        # Если валидация для недели
        if inp["group_type"] == "week":
            val = 0
            week_start = dt_from_obj
            week_end = week_start + datetime.timedelta(days=6)
            while week_end <= dt_to_obj:
                for i in right_data:
                    if week_start <= i["dt"] <= week_end:
                        val += i["value"]

                answer["dataset"].append(val)
                val = 0
                answer["labels"].append(week_start.strftime("%Y-%m-%d"))

                week_start += datetime.timedelta(days=7)
                week_end += datetime.timedelta(days=7)

        # Если валидация для дня
        if inp["group_type"] == "day":
            val = 0
            for j in range((dt_to_obj - dt_from_obj).days + 1):
                for i in right_data:
                    if i["dt"].date() == (dt_from_obj + datetime.timedelta(days=j)).date():
                        val += i["value"]

                answer["dataset"].append(val)
                val = 0
                answer["labels"].append((dt_from_obj + datetime.timedelta(days=j)).isoformat())

        # Если валидация для часa
        if inp["group_type"] == "hour":
            val = 0
            for j in range(round((dt_to_obj - dt_from_obj).total_seconds() / 3600) + 1):
                for i in right_data:
                    if i["dt"].hour == (dt_from_obj + datetime.timedelta(hours=j)).hour and i["dt"].date() == (
                            dt_from_obj + datetime.timedelta(hours=j)).date():
                        val += i["value"]

                answer["dataset"].append(val)
                val = 0
                answer["labels"].append((dt_from_obj + datetime.timedelta(hours=j)).isoformat())

    f.close()
    return json.dumps(answer)


