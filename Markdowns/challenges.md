# Challenges Faced

- [Challenges Faced](#challenges-faced)
    - [Monthly Usage based on Weekly Usage](#monthly-usage-based-on-weekly-usage)

### Monthly Usage based on Weekly Usage

##### Solution Fixed - 8/16/18

Removed it from program and used some of this code block to build a similar function based on daily occurrences

##### Problem

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

This function, `new_monthly_usage()`, was part of my Weekly Usage class and was made to make new monthly usage data based off the weekly
usage data. First it would take the user id, `uid`, and query for all weekly usage in the database and stores it as list of dictionary
objects in the variable `dates`. Next, another variable, `m_usage`, was created and given a value of 0. The function iterates over `dates`
through Python's `enumerate()` function thereby creating two new variables, `position` - the numerical index in `dates`, and `item` -
the actual value of the index in `dates`. `new_monthly_usage()` extracts the month property of `item`, stores it in `monthly` and sets
`number_of_weeks` to 0. Another loop loops through `dates` starting from index `position` until `dates[position]`'s month property
changes. Inside this loop `number_of_weeks` increments by 1 every time the statement is true. The function checks the to see if there are
at least 4 consecutive weeks for the respective month in the database if not it restarts the `for` loop with the next iteration.
Ultimately, this function proved useless because a week can start in one month and end in another. For example, the week of July 29,
2018 starts in the month of July by ends in the month of August, August 4, 2018. Additionally, a week can even start and end in different
years. Thus this function becomes useless. 

[Back to Top](#challenges-faced)

