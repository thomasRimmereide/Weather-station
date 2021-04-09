import pickle

a = {"day_bergen": 1, "day_oslo": 1, "day_stavanger": 1, "month_bergen": "May",
     "month_oslo": "May", "month_stavanger": "May", "year_bergen": 1981,
     "year_oslo": 1981, "year_stavanger": 1981}


def save_today_date(today_date=dict()):
    d = update_today_date()
    d.update(today_date)
    file = open("../Database_files/current_date.pickle", "wb")
    pickle.dump(d, file)
    file.close()


def update_today_date():
    with open("../Database_files/current_date.pickle", "rb") as data:
        today = data.read()
    d = pickle.loads(today)
    return d


save_today_date(a)
update_today_date()
