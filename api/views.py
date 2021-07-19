from django.shortcuts import render
from xbbg import blp
from .forms import BBForm

def BloombergAPI(request):
    if request.method == 'GET':
        form = BBForm()
        return render(request, 'api/bloomberg_api.html', {'form': form})

    elif request.method == 'POST':
        form = BBForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data['ticker']
            variable = form.cleaned_data['variable']
            start_date = form.cleaned_data['start_date'].strftime('%Y-%m-%d')
            end_date = form.cleaned_data['end_date'].strftime('%Y-%m-%d')
            data = blp.bdh(tickers=ticker, flds=variable, start_date=start_date, end_date=end_date)
            html_data = data[ticker][variable].to_list()
            labels = data.index.strftime('%Y-%m-%d').to_list()
            form = BBForm()
        return render(request, 'api/bloomberg_api.html', {'data': html_data, 'labels': labels, 'variable': variable, 'ticker': ticker, 'form': form})