from django.shortcuts import render

# Create your views here.



def dataFormulate(request):

    #지훈이 코드 여기에

    return render(request, "MainPage.html") #모델 함께 넘겨줘야함.

def guInfoCreate(request):
    gu_dict = ['종로구','중구','용산구','성동구','광진구','동대문구','중랑구','성북구','강북구','도봉구','노원구','은평구','서대문구','마포구','양천구','강서구','구로구','금천구','영등포구','동작구','관악구','서초구','강남구','송파구','강동구']


    for i in gu_dict:
        with open("gu/"+i+".txt","r", encoding='utf-8') as f:
            Lines = f.readline()
            dongList = Lines.split(",")
            print(dongList)

    return render(request, "MainPage.html")
