from django.shortcuts import render,redirect
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.preprocessing import LabelEncoder

import plotly.io as pio
pio.templates.default = 'plotly_dark'

import pandas as pd
import numpy as np
import requests
from urllib.parse import urlparse
import urllib.parse
import time
import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine
import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls

# Create your views here.

lgb_model = ""
predictedValue = ''
predictedGu = ""
predictedDong = ""
predictedApt = ""
parkMapLink = ''

def backtoHome(request):

    return render(request, "index.html")

def dongTest(request):
        selected_gu = request.GET['selected_gu']

        data = pd.read_csv('final_end.csv',index_col = 0)
        seoulDongList = data["dong"].unique()

        dongList = []

        with open("gu/"+selected_gu+".txt","r", encoding='utf-8') as f:
            Lines = f.readline()
            selectdDongList = Lines.split(",")

        finalDongList = []
        for i in seoulDongList:
            if i in selectdDongList:
                finalDongList.append(i)

        return render(request, "dongSelect.html",{"dongInfo":finalDongList,"guSelected": selected_gu})





def dataFormulate(request):
    data = pd.read_csv('data.csv',index_col = 0)

    from sklearn.model_selection import train_test_split
    Y = data['price(manwon)']
    X = data.drop('price(manwon)',axis=1)
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.1 , random_state = 1234)

    train_ds = lgb.Dataset(X_train,label=Y_train)
    test_ds = lgb.Dataset(X_test,label=Y_test)
    params = {"objective" : "regression", "metric" : "mse", 'n_estimators':1000,"num_leaves" : 20, "learning_rate" : 0.1, "bagging_fraction" : 0.8, 'max_depth': 6}#15000번 테스트
    global lgb_model
    lgb_model = lgb.train(params, train_ds, 1000, test_ds, verbose_eval=1000, early_stopping_rounds=100)

    return redirect("main:guSelect")

#기타 정보입력받는 뷰
def extraInfo_select(request):

    selected_gu = request.POST['guSelected']
    selected_dong = request.POST['dongSelected']
    selected_apt = request.POST['slct']

    return render(request, "extraSelect.html",{"aptSelected": selected_apt, "dongSelected":selected_dong,"guSelected": selected_gu})

def predictInput(request):
        selected_gu = request.POST['guSelected']
        selected_dong = request.POST['dongSelected']
        selected_apt = request.POST['aptSelected']
        selectedDate = request.POST['dateSelected']
        selectedSize = int(request.POST['sizeSelected']) *  3.31

        selectedYear, selectedMonth = map(int,selectedDate.split("-"))

        #아파트랑 구 번호로 변환

        data = pd.read_csv('final_end.csv')

        dong_enc = LabelEncoder().fit_transform(data['dong'])
        apt_name_enc = LabelEncoder().fit_transform(data['apt_name'])

        dong_num = pd.DataFrame({'enc':dong_enc,'dong':pd.read_csv('final_end.csv')['dong']})
        dong_num = dong_num.drop_duplicates().reset_index(drop=True)
        found_dong_num = int(dong_num[dong_num['dong']==selected_dong]['enc'])

        apt_num = pd.DataFrame({'enc':apt_name_enc,'apt':pd.read_csv('final_end.csv')['apt_name']})
        apt_num = apt_num.drop_duplicates().reset_index(drop=True)
        found_apt_num =  int(apt_num[apt_num['apt']==selected_apt]['enc'])

        result = price_pred(x1=selectedYear,x2=selectedMonth,x3=found_dong_num,x4=found_apt_num, x5=selectedSize)
        price = result[0]
        global predictedValue
        global predictedGu
        global predictedDong
        global predictedApt
        global parkMapLink
        predictedGu = selected_gu
        predictedDong = selected_dong
        predictedApt = selected_apt
        predictedValue = str(int(price // 10000))+ "억 "+str(int(price % 10000)) + "만원"

        try:
            parkMapLink = parkMapInfoCreate(predictedApt)
        except:
            parkMapLink = ''

        return redirect("main:guSelect")

#최종화면에서 가격예측해주는 함수
def price_pred(x1, x2,x3,x4, x5=77.95, x6=0,x7=0,x8=0,x9=9,x10=1998):
    mmm=[{'use_area(m2)': x5, 'transaction_year':x1,'transaction_month':x2, 'date(1~10)':x6,'date(11~20)':x7,'date(21~)':x8,'floor':x9,'year_found':x10,'dong_enc':x3,'apt_name_enc':x4}]
    inp=pd.DataFrame(mmm)
    global lgb_model
    return lgb_model.predict(inp)

#동선택 뷰
def dong_select(request):

    selected_gu = request.POST['slct']

    data = pd.read_csv('final_end.csv',index_col = 0)
    seoulDongList = data["dong"].unique()

    dongList = []

    with open("gu/"+selected_gu+".txt","r", encoding='utf-8') as f:
        Lines = f.readline()
        selectdDongList = Lines.split(",")

    finalDongList = []
    for i in seoulDongList:
        if i in selectdDongList:
            finalDongList.append(i)

    return render(request, "dongSelect.html",{"dongInfo":finalDongList,"guSelected": selected_gu})

def apt_select(request):

    selected_gu = request.POST['guSelected']
    selected_dong = request.POST['slct']

    data = pd.read_csv('final_end.csv',index_col = 0)

    grouped = data.groupby('dong').get_group(selected_dong)["apt_name"].unique()

    return render(request, "aptSelect.html", {"aptInfo":grouped, "guSelected" : selected_gu, "dongSelected" : selected_dong})


def guInfoCreate(request):
    gu_dict = ['종로구','중구','용산구','성동구','광진구','동대문구','중랑구','성북구','강북구','도봉구','노원구','은평구','서대문구','마포구','양천구','강서구','구로구','금천구','영등포구','동작구','관악구','서초구','강남구','송파구','강동구']

    global predictedValue
    global predictedGu
    global predictedDong
    global predictedApt
    global parkMapLink

    predicted = predictedValue
    # for i in gu_dict:
    #     with open("gu/"+i+".txt","r", encoding='utf-8') as f:
    #         Lines = f.readline()
    #         dongList = Lines.split(",")
    #         print(dongList)

    return render(request, "index.html", {"guInfo":gu_dict, "predictedPrice": predicted, "predictedGu":predictedGu,  "predictedDong":predictedDong,  "predictedApt":predictedApt, 'parkMapLink' : parkMapLink})

def parkMapInfoCreate(address):
    apt_address = pd.read_csv('apt_address.csv')
    park_after = pd.read_csv('parkWithLatLng_after.csv',usecols = ['city','gu','dong','park_name','park_type','park_area','name','id','lat','lng'])

    username='Jeehoon-K'
    api_key= '2mJ6DMkHJjm1oGEBYyn2'
    chart_studio.tools.set_credentials_file(username=username,api_key=api_key)
    fig = get_map(address, park_after,apt_address)
    return py.plot(fig, filename = 'Monochrome', auto_open=False)

def id(name, apt_address):
  address = apt_address[apt_address['apt_name']==str(name)].reset_index()['address'][0]
  url = 'https://dapi.kakao.com/v2/local/search/address.json?&query=' + str(address)
  result = requests.get(urlparse(url).geturl(), headers={'Authorization': 'KakaoAK 10faa6da25b75ef0a75b555ae4e5d64e'}).json()
  match_first = result['documents'][0]['address']
  lat = float(match_first['y'])
  lng = float(match_first['x'])
  return [lat, lng]

def get_close_index(apt_name, park_after, apt_address):
  P = park_after['lat']-id(apt_name, apt_address)[0]
  Q = park_after['lng']-id(apt_name, apt_address)[1]
  s = [k for k in range(len(park_after)) if -0.01<P[k]<0.01]
  l = [k for k in s if -0.02<Q[k]<0.02]
  f = [k for k in l if haversine(id(apt_name,apt_address), [park_after['lat'][k],park_after['lng'][k]], unit = 'm') <= 500]
  return f

def get_map(address, park_after, apt_address):
  f = get_close_index(address, park_after,apt_address)
  C = []
  for k in range(len(park_after)):
    if k not in f:
      C.append('공원')
    else:
      C.append('근방 공원')

  park_after['color']=C

  px.set_mapbox_access_token('pk.eyJ1Ijoiam9objEwMTAxMCIsImEiOiJja2tjOXN5OG0wbDA2Mm5wODVhZ3R1OW5rIn0.j37zc9C6hM8DCo0fLlRirg')

  data = park_after.copy()
  data['park_area'] = np.log(data['park_area'])
  fig = go.Figure()
  fig = px.scatter_mapbox(data, lat="lat", lon="lng",
                          size= "park_area",
                          hover_name="name",
                          size_max=15,
                          zoom=13,
                          center={'lat':id(address,apt_address)[0],'lon':id(address,apt_address)[1]},
                          color = 'color',
                          title = '내 아파트 주변 공원'
                          )
  fig.update_layout(mapbox_style="carto-darkmatter")


  return fig
