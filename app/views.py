from datetime import datetime
from django.shortcuts import render
from .models import Stoke
from django.db.models import Sum
import requests
import json

dates = ['17-Jun-2021', '24-Jun-2021', '01-Jul-2021', '08-Jul-2021', '15-Jul-2021', '22-Jul-2021',
         '29-Jul-2021', '05-Aug-2021', '12-Aug-2021', '26-Aug-2021', '30-Sep-2021', '30-Dec-2021',
         '31-Mar-2022', '30-Jun-2022', '29-Dec-2022', '29-Jun-2023', '28-Dec-2023', '27-Jun-2024',
         '26-Dec-2024', '26-Jun-2025', '24-Dec-2025']

conv_date = {}
for date in dates:
    conv_date[date] = str(datetime.strptime(date, '%d-%b-%Y').date())
Prices = [6000, 7500, 7600, 8000, 8100, 8200, 8300, 8400, 8500, 8600, 8700, 8800, 8900, 9000, 9100, 9200, 9300, 9400,
          9500, 9600, 9700, 9800, 9900, 10000, 10100, 10200, 10300, 10400, 10500, 10600, 10700, 10800, 10900, 11000,
          11100, 11200, 11300, 11400, 11500, 11600, 11700, 11800, 11900, 12000]


def collect(var):
    try:
        new_url = 'https://www.nseindia.com/api/option-chain-indices?symbol=%s' % var
        headers = {'User-Agent': 'Chrome/91.0.4472.77'}
        page = requests.get(new_url, headers=headers)
        dajs = json.loads(page.text)

    except:
        return

    for expiry_dt in dajs['records']['expiryDates']:

        for data in dajs['records']['data']:
            stoke = Stoke()
            if 'CE' in data and 'PE' in data and data['expiryDate'] == expiry_dt:
                stoke.strikePrice = data['CE']['strikePrice']
                stoke.Option = data['CE']['underlying']
                stoke.c_Oi = data['CE']['openInterest']
                stoke.c_ChangeInOi = data['CE']['changeinOpenInterest']
                stoke.c_Volume = data['CE']['totalTradedVolume']
                stoke.c_Iv = data['CE']['impliedVolatility']
                stoke.c_Ltp = data['CE']['lastPrice']
                stoke.c_Chng = data['CE']['change']
                stoke.c_BidQty = data['CE']['bidQty']
                stoke.c_BidPrice = data['CE']['bidprice']
                stoke.c_AskPrice = data['CE']['askQty']
                stoke.c_AskQty = data['CE']['askPrice']
                stoke.p_Oi = data['PE']['openInterest']
                stoke.p_ChangeInOi = data['PE']['changeinOpenInterest']
                stoke.p_Volume = data['PE']['totalTradedVolume']
                stoke.p_Iv = data['PE']['impliedVolatility']
                stoke.p_Ltp = data['PE']['lastPrice']
                stoke.p_Chng = data['PE']['change']
                stoke.p_BidQty = data['PE']['bidQty']
                stoke.p_BidPrice = data['PE']['bidprice']
                stoke.p_AskPrice = data['PE']['askQty']
                stoke.p_AskQty = data['PE']['askPrice']

                stoke.expiry_dt = datetime.strptime(expiry_dt, '%d-%b-%Y').date()
                stoke.save()

            elif 'CE' in data and data['expiryDate'] == expiry_dt:
                # ['id', 'strikePrice', 'Option', 'expiry_dt', 'c_Oi', 'c_ChangeInOi', 'c_Volume', 'c_Iv', 'c_Ltp',
                #  'c_Chng', 'c_BidQty', 'c_BidPrice', 'c_AskPrice', 'c_ASkQty']

                stoke.strikePrice = data['CE']['strikePrice']
                stoke.Option = data['CE']['underlying']
                stoke.c_Oi = data['CE']['openInterest']
                stoke.c_ChangeInOi = data['CE']['changeinOpenInterest']
                stoke.c_Volume = data['CE']['totalTradedVolume']
                stoke.c_Iv = data['CE']['impliedVolatility']
                stoke.c_Ltp = data['CE']['lastPrice']
                stoke.c_Chng = data['CE']['change']
                stoke.c_BidQty = data['CE']['bidQty']
                stoke.c_BidPrice = data['CE']['bidprice']
                stoke.c_AskPrice = data['CE']['askQty']
                stoke.c_AskQty = data['CE']['askPrice']
                stoke.expiry_dt = datetime.strptime(expiry_dt,
                                                    '%d-%b-%Y').date()  # print(datetime.strptime(expiry_dt, '%Y-%m-%d'))
                # print("ce",stoke,data['CE']['strikePrice'])

                stoke.save()

            elif 'PE' in data and data['expiryDate'] == expiry_dt:
                stoke.strikePrice = data['PE']['strikePrice']
                stoke.Option = data['PE']['underlying']
                stoke.p_Oi = data['PE']['openInterest']
                stoke.p_ChangeInOi = data['PE']['changeinOpenInterest']
                stoke.p_Volume = data['PE']['totalTradedVolume']
                stoke.p_Iv = data['PE']['impliedVolatility']
                stoke.p_Ltp = data['PE']['lastPrice']
                stoke.p_Chng = data['PE']['change']
                stoke.p_BidQty = data['PE']['bidQty']
                stoke.p_BidPrice = data['PE']['bidprice']
                stoke.p_AskPrice = data['PE']['askQty']
                stoke.p_AskQty = data['PE']['askPrice']
                stoke.expiry_dt = datetime.strptime(expiry_dt,
                                                    '%d-%b-%Y').date()  # print(datetime.strptime(expiry_dt, '%Y-%m-%d'))
                # print("pe",stoke,data['PE']['strikePrice'])

                stoke.save()

    print("fetched for ", var)


def collect_category():
    vars = ['NIFTY','BANKNIFTY', 'FINNIFTY']
    Stoke.objects.all().delete()
    for var in vars:
        collect(var)


def detail(request):
    # if you want to get the data don't comment the below function
    # otherwise comment it.
    # collect_category()
    stokes=Stoke.objects.all()
    opt_filter = None
    exp_filter = None
    sp_filter = None
    if request.GET.get('options') and request.GET.get('options') != 'select':
        opt_filter = request.GET.get('options')
        stokes = stokes.filter(Option=opt_filter)

    if request.GET.get('expiry_dt') and request.GET.get('expiry_dt') != 'select':
        exp_filter = request.GET.get('expiry_dt')
        date = datetime.strptime(exp_filter, '%Y-%m-%d')
        stokes = stokes.filter(expiry_dt=date)

    if request.GET.get('strikePrice') and request.GET.get('strikePrice') != 'select':
        exp_filter = None
        sp_filter = request.GET.get('strikePrice')
        stokes = stokes.filter(strikePrice=sp_filter)
    c_Oi_sum=stokes.aggregate(Sum('c_Oi'))['c_Oi__sum']
    c_Volume_sum=stokes.aggregate(Sum('c_Volume'))['c_Volume__sum']
    p_Oi_sum = stokes.aggregate(Sum('p_Oi'))['p_Oi__sum']
    p_Volume_sum = stokes.aggregate(Sum('p_Volume'))['p_Volume__sum']
    context_dict = {'stokes': stokes, 'conv_date': conv_date, 'Prices': Prices,'c_Oi_sum':c_Oi_sum,'c_Volume_sum':c_Volume_sum,'p_Oi_sum':p_Oi_sum,'p_Volume_sum':p_Volume_sum}
    if opt_filter:
        context_dict['opt_filter'] = opt_filter
    if exp_filter:
        context_dict['exp_filter'] = exp_filter
    elif sp_filter:
        context_dict['sp_filter'] = sp_filter
    # return render(request, template_name, context_dict)
    return render(request, 'app/detail.html', context_dict)
