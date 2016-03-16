import pygal
import json
from urllib import urlopen  # python 2 syntax
# from urllib.request import urlopen # python 3 syntax
import pandas as pd
 
from flask import Flask, render_template, request
from pygal.style import DarkSolarizedStyle
 
app = Flask(__name__)


#----------------------------------------------------------------------
@app.route('/graph',methods=['GET','POST'])
def FC_data():
    
    #cty = request.form['cty']
    #vbl = request.form['vbl']
    
    country = 'Nepal'
    var = 'FR'
    
    if request.method == 'POST':
      country = request.form.get['cty']
      var = request.form.get['vbl']
    
    cdata = pd.read_csv('Country-Data.csv')
    cdata = cdata[cdata.Country == country]

    if var == 'FC':
      var_full = 'Occupational Fatality Count'
    else:
      var_full = 'Occupational Fatality Rate'
    
    # create a bar chart
    title = '%s for %s' % (var_full, country)
    bar_chart = pygal.Bar(width=900, height=450,
                          explicit_size=True, title=title, style=DarkSolarizedStyle, legend_at_bottom=True)
 
    vari = cdata[var]

    bar_chart.x_labels = cdata["year"]
    bar_chart.add(var_full, vari) 
    #bar_chart.add('GDP Per Capita', gdppc) 
    
    html = """
        <html>
        <link rel=stylesheet type=text/css href='{{ url_for('static',filename='style_lulu.css')}}'>
                <form method='post' action='graph'>
                Select Country: <select name='cty'>
                    <option value="United States">United States</option>
                    <option value="Nepal">Nepal</option>
                    <option value="Jamaica">Jamaica</option>
                    <option value="Nigeria">Nigeria</option>
                </select><br>
                Select Variable: <select name='vbl'>
                    <option value="FR">Occupational Fatality Rate</option>
                    <option value="FC">Occupational Fatality Count</option>
                </select><br>
                 <input type='submit' value='submit' />
                </form>
             <head>
                  <title>%s</title>
             </head>
              <body>
                 %s
             </body>
        </html>
        """% (title, bar_chart.render())
    return html
#----------------------------------------------------------------------
if __name__ == '__main__':    
    app.run()