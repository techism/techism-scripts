import locale
import calendar
import codecs
import datetime


locale.setlocale(locale.LC_ALL, 'de_DE.utf8')

labels = []

CURRENT_YEAR = datetime.datetime.now().year

def write_calendar ():
    for month in range(1,13):
        if month % 3 == 1:
            labels.append('<div class="line">')
        labels.append('<div class="month">')
        write_month (month)
        labels.append("</div>")
        if month % 3 == 0:
            labels.append("</div>")
        labels.append('\n')


def write_month (month):
    month_name = calendar.month_name[month].decode("utf8")
    href = '/events/' + str(CURRENT_YEAR) + '/' + str(month) + '/'
    labels.append('<div><a class="month_title_link" href="' + href + '">' + month_name.lower() + '</a></div>')
    cal = calendar.Calendar ()
    for day in cal.itermonthdays(CURRENT_YEAR, month):
        write_day (month, day)
    


def write_day (month, day):
    if day > 0:
        str_day = str(day)
        if (day < 10):
            str_day = '0' + str_day
        current_weekday = calendar.weekday(CURRENT_YEAR, month, day)
        href = '/events/' + str(CURRENT_YEAR) + '/' + str(month) + '/' + str(day) + '/'

        attr_class = get_day_class_attribute(CURRENT_YEAR, month, day, current_weekday)

        labels.append('<a' + attr_class + ' href="' + href + '">' + str_day + '</a>')
        if current_weekday == 6:
           labels.append('<br/>')
    else:
        labels.append('<label>&nbsp;</label>');


def get_day_class_attribute (year, month, day, current_weekday):
    #str_year = str(year)
    #str_month = str(month)
    #if (month < 10):
    #        str_month = '0' + str_month
    #str_day = str(day)
    #if (day < 10):
    #        str_day = '0' + str_day
    #attr_class = 'd' + str_year + str_month + str_day
    if current_weekday == 6 or current_weekday == 5:
        attr_class = "day_weekend"
        return ' class="' + attr_class + '"'
    else:
        return '';


with codecs.open('calendarfragment.html', 'w', 'utf-8') as f:
    f.write('<html><head>')
    f.write('<link rel="stylesheet" type="text/css" href="calendar.css">')
    f.write('</head>')
    write_calendar()
    for entry in labels:
        f.write(entry)
        f.write(' ')
    f.write('</html>')
