import aiohttp

from config import email, api_key

weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


async def create_lead(user_data):
    async with aiohttp.ClientSession() as session:
        async with session.post('https://geniusekb.s20.online/v2api/auth/login',
                                json={'email': email,
                                      'api_key': api_key
                                      }) as resp:
            response = await resp.json()
            api_token = response["token"]
        days = ""
        for i in range(7):
            if user_data["days_data"][i] == 1:
                days += weekdays[i] + ", "
        days = days[:-2]
        note = f"""Возраст ребенка: {user_data['age']}
Дни: {days}
Время: {user_data['time']}
Кол-во дней: {user_data['days_count']}"""
        async with session.post('https://geniusekb.s20.online/v2api/1/customer/create',
                                headers={'X-ALFACRM-TOKEN': api_token,
                                         'Content-Type': 'application/json'},
                                json={'name': user_data["phone"],
                                      "legal_type": 1,
                                      "is_study": 0,
                                      "branch_ids": [1],
                                      "phone": [user_data["phone"]],
                                      "note": note
                                      }) as resp:
            response = await resp.json()