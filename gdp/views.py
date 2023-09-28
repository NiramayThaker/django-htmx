from django.shortcuts import render
from django.db.models import Max 
from .models import GDP
from bokeh.models import ColumnarDataSource
from bokeh.embed import components
from bokeh.plotting import figure


# Create your views here.
def index(request):
    max_year = GDP.objects.aggregate(max_yr=Max('year'))
    year = request.GET.get('year', max_year)

    count = int(request.GET.get('count', 10))
    gdps = GDP.objects.filter(year=year).order_by('gdp').reverse()[:count]

    country_names = [d.country for d in gdps]
    country_gdps = [d.gdp for d in gdps]

    cds = ColumnarDataSource(data=dict(country_names=country_names, country_gdps=country_gdps))

    fig = figure(x_range=country_names, height=500, title=f"Top {count} GDPs ({year})")
    fig.vbar(source=cds, x='country_names', y='country_gdps', width=0.8)

    script, div = components(fig)

    context = {
        'script': script,
        'div': div,
    }

    return render(request, 'index.html', context=context)
