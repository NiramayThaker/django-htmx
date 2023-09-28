from django.shortcuts import render
from django.db.models import Max, Min
from .models import GDP
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.embed import components
from bokeh.plotting import figure
import math 


# Create your views here.
def index(request):
    # max_year = GDP.objects.aggregate(max_yr=Max('year'))['max_yr']
    max_year = GDP.objects.aggregate(max_yr=Max('year'))['max_yr']
    min_year = GDP.objects.aggregate(min_yr=Min('year'))['min_yr']
    year = request.GET.get('year', max_year)

    count = int(request.GET.get('count', 10))
    gdps = GDP.objects.filter(year=year).order_by('gdp').reverse()[:count]

    country_names = [d.country for d in gdps]
    country_gdps = [d.gdp for d in gdps]

    cds = ColumnDataSource(data=dict(country_names=country_names, country_gdps=country_gdps))

    fig = figure(x_range=country_names, height=500, title=f"Top {count} GDPs ({year})")
    fig.vbar(source=cds, x='country_names', top='country_gdps', width=0.8)
    fig.yaxis[0].formatter = NumeralTickFormatter(format="$0.0a")
    fig.xaxis.major_label_orientation = math.pi / 4
    

    script, div = components(fig)

    
    context = {
        'script': script,
        'div': div,
        'year': range(min_year, max_year + 1)
    }

    return render(request, 'index.html', context=context)
