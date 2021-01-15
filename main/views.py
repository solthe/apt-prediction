from django.shortcuts import render
import pandas as pd
import numpy as np
import lightgbm as lgb

# Create your views here.

lgb_model = ""



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

    return render(request, "MainPage.html")


#최종화면에서 가격예측해주는 함수
def price_pred(x1, x2,x3,x4, x5=77.95, x6=0,x7=0,x8=0,x9=9,x10=1998):
    mmm=[{'transaction_year':x1,'transaction_month':x2,'dong_enc':x3,'apt_name_enc':x4,'use_area(m2)': x5,'date(1~10)':x6,'date(11~20)':x7,'date(21~)':x8,'floor':x9,'year_found':x10}]
    inp=pd.DataFrame(mmm)
    global lgb_model
    return lgb_model.predict(inp)

def dong_select(request):

    data = pd.read_csv('final_end.csv',index_col = 0)
    seoulDongList = data["dong"].unique()

    selected_gu = "성북구"#리퀘스트에서 넘어와야함

    dongList = []

    with open("gu/"+selected_gu+".txt","r", encoding='utf-8') as f:
        Lines = f.readline()
        selectdDongList = Lines.split(",")

    finalDongList = []
    for i in seoulDongList:
        if i in selectdDongList:
            finalDongList.append(i)

    print(finalDongList)

    return render(request, "MainPage.html")

def apt_select(request):

    selected_dong = "돈암동"#reqeust에서 넘어와야함

    data = pd.read_csv('final_end.csv',index_col = 0)

    grouped = data.groupby('dong').get_group(selected_dong)["apt_name"].unique()
    print(grouped)

    return render(request, "MainPage.html")


def guInfoCreate(request):
    gu_dict = ['종로구','중구','용산구','성동구','광진구','동대문구','중랑구','성북구','강북구','도봉구','노원구','은평구','서대문구','마포구','양천구','강서구','구로구','금천구','영등포구','동작구','관악구','서초구','강남구','송파구','강동구']


    for i in gu_dict:
        with open("gu/"+i+".txt","r", encoding='utf-8') as f:
            Lines = f.readline()
            dongList = Lines.split(",")
            print(dongList)

    return render(request, "MainPage.html")
