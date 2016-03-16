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
    
    country = 'United States'
    var = 'FR'
    
    if request.method == 'POST':
      country = request.form.get('cty')
      var = request.form.get('vbl')
      
      #country = (request.form.get['cty'])
      #var = (request.form.get['vbl'])
    
    cdata = pd.read_csv('Country-Data.csv')
    cdata = cdata[cdata.Country == country]

    if var == 'FC':
      var_full = 'Occupational Fatality Count'
      var_t = 'Occupational Fatality Count'
    else:
      var_full = 'Occupational Fatality Rate'
      var_t = 'Occupational Fatality Rate (Per 100,000 Workers)'
    
    # create a bar chart
    title = '%s for %s' % (var_t, country)
    bar_chart = pygal.Bar(width=900, height=450,
                          explicit_size=True, title=title, style=DarkSolarizedStyle, legend_at_bottom=True)
 
    vari = cdata[var]

    bar_chart.x_labels = cdata["year"]
    bar_chart.add(var_full, vari)
    chart=bar_chart.render(is_unicode=True)
    return render_template('graph.html', tit = title, chart=chart)
#----------------------------------------------------------------------
if __name__ == '__main__':    
    app.run()