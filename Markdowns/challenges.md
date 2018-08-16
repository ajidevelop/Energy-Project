````python
@classmethod
def new_monthly_usage(cls, uid):
    dates = cls.query.filter_by(uid=uid).order_by(cls.week_start_year, cls.week_start_month, cls.week_start_day).all()
    m_usage = 0
    for position, item in enumerate(dates):
        monthly = item.week_start_date.strftime('%m')
        number_of_weeks = 0
        while dates[position + number_of_weeks].week_start_date.strftime('%m') == monthly:
            number_of_weeks += 1
        if number_of_weeks < 4:
            continue
        try:
            month = []
            for i in range(len(dates[position: position + number_of_weeks])):
                if i == 0:
                    month.append(dates[position])
                    m_usage += month[i].w_usage
                    continue
                weeks = dates[position + i].week_start_date - dates[position + i - 1].week_start_date
                if weeks.days == 7:
                    month.append(dates[position + i])
                    m_usage += month[i].w_usage
                else:
                    m_usage = 0
                    break
        except AttributeError:
            pass
        else:
            if len(month) >= 4:
                MonthUsage.new_month_entry(datetime.date(month[0].week_start_year, month[0].week_start_month, 1), m_usage, uid)
                m_usage = 0
            else:
                m_usage = 0
````


~~~html
.bot {
    border: none;
}
~~~



