import locale
import calendar
import codecs

locale.setlocale(locale.LC_ALL, 'de_DE.utf8')

labels = []
for i in range(1,13):
    month = calendar.month_name[i].decode("utf8")
    labels.append('<a href="">' + month + '</a>')
    cal = calendar.Calendar ()
    for day in cal.itermonthdays(2013, i):
        if day > 0:
            labels.append(str(day))

with codecs.open('calendarfragment.html', 'w', 'utf-8') as f:
    for entry in labels:
        print entry
        f.write(entry)
        f.write(' ')
