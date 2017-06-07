from flask import Flask, render_template
from datetime import datetime
import csv
import collections


app = Flask(__name__)

@app.route('/')
def main():
    all_dates = {}
    with open('askhistorians.csv', 'rt') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if  'date' in row:
                try:
                    time = datetime.strptime(row['date'],'%Y-%m-%d %H:%M:%S-05:00')
                except:
                    time = datetime.strptime(row['date'],'%Y-%m-%d %H:%M:%S-04:00')
                current_date = datetime.date(time)
                if current_date in all_dates:
                    all_dates[current_date] += 1
                else:
                    all_dates[current_date] = 1

    od = collections.OrderedDict(sorted(all_dates.items()))
    dates = list(od.keys())
    dates = [date.strftime('%b %d,%Y') for date in dates]
    numposts = list(od.values())
    graph_values = [{'x': dates, 'y': numposts, 'type': 'bar'}]

    return render_template('index.html', graph_values=graph_values)

if __name__ == '__main__':
  app.run(debug= True,host="127.0.0.1",port=5000, threaded=True)
