from django.shortcuts import render,redirect
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.preprocessing import LabelEncoder

# Create your views here.

lgb_model = ""

def backtoHome(request):

    return render(request, "MainPage.html")



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

    return redirect("main:home")

#기타 정보입력받는 뷰
def extraInfo_select(request):

    selected_gu = request.POST['guSelected']
    selected_dong = request.POST['dongSelected']
    selected_apt = request.POST['slct']

    print(selected_gu,selected_dong,selected_apt)

    return render(request, "extraSelect.html",{"aptSelected": selected_apt, "dongSelected":selected_dong,"guSelected": selected_gu})

def predictInput(request):
        selected_gu = request.POST['guSelected']
        selected_dong = request.POST['dongSelected']
        selected_apt = request.POST['aptSelected']
        selectedDate = request.POST['dateSelected']
        selectedSize = int(request.POST['sizeSelected']) *  3.31

        selectedYear, selectedMonth = map(int,selectedDate.split("-"))

        #아파트랑 구 번호로 변환

        print(selected_gu,selected_dong,selected_apt,selectedDate,selectedSize)
        data = pd.read_csv('final_end.csv')

        dong_enc = LabelEncoder().fit_transform(data['dong'])
        apt_name_enc = LabelEncoder().fit_transform(data['apt_name'])

        dong_num = pd.DataFrame({'enc':dong_enc,'dong':pd.read_csv('final_end.csv')['dong']})
        dong_num = dong_num.drop_duplicates().reset_index(drop=True)
        found_dong_num = int(dong_num[dong_num['dong']==selected_dong]['enc'])

        apt_num = pd.DataFrame({'enc':apt_name_enc,'apt':pd.read_csv('final_end.csv')['apt_name']})
        apt_num = apt_num.drop_duplicates().reset_index(drop=True)
        found_apt_num =  int(apt_num[apt_num['apt']==selected_apt]['enc'])

        print(found_dong_num,found_apt_num)

        result = price_pred(x1=selectedYear,x2=selectedMonth,x3=found_dong_num,x4=found_apt_num, x5=selectedSize)
        print(result,"만원")
        return redirect("main:home")

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


    # for i in gu_dict:
    #     with open("gu/"+i+".txt","r", encoding='utf-8') as f:
    #         Lines = f.readline()
    #         dongList = Lines.split(",")
    #         print(dongList)

    return render(request, "guSelect.html", {"guInfo":gu_dict})
