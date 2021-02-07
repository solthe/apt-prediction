# YBigta 학회 DA팀 2021 겨울방학 프로젝트
## Members
  * 김형준 (https://github.com/Joon-Kim-Lang)    
  * 최은솔 (https://github.com/solthe)   
  * 김지훈 (https://github.com/Jeehoon-K) 
# Seoul Apartment price prediction project

# About
  이 프로젝트는 연세대학교 빅데이터학회 Ybigta Data Analytics팀 2021년 겨울방학 프로젝트로,
  2008년부터 2020년까지의 아파트 거래정보 데이터를 활용하여 추후 가격을 예측하는 모델을 만들고
  장고 웹 프레임워크를 활용하여 사용자에게 가격예측 서비스를 제공하고 다양한 시각화 자료를
  제공함.   
     
  * Data origin :   
    * [2008~2017년 실거래가](https://dacon.io/competitions/official/21265/data/)   
    * [2017~2020년 실거래가](https://rt.molit.go.kr/)   
    * [공원 데이터](https://dacon.io/competitions/official/21265/data/)
  
# Overall Flow
![image](https://user-images.githubusercontent.com/61021101/106378798-ca274380-63ea-11eb-931a-56a303b5b3a6.png)

# Data Processing & Analysis
## 1)아파트 실거래가 분석모델
![image](https://user-images.githubusercontent.com/61021101/106378867-589bc500-63eb-11eb-970d-c880cc66b5ca.png)
* **data processing**   
  * 'transaction_day' : 'date(1\~10)','date(11\~20)','date(21~)'로 one-hot encoding   
  * 'dong','apt_name' : 'dong_enc','apt_name_enc'로 Label encoding   
  * 'price' : ex. 315,000 (object) -> 315000 (int)   
  * variable correlation : Nan (threshold : |0.2|)


![image](https://user-images.githubusercontent.com/61021101/106378868-5d607900-63eb-11eb-8cd6-350c5231d7f4.png)
* **model**   
  * LightGBM   
  * params = {"objective" : "regression", "metric" : "mse", 'n_estimators':15000,
              "num_leaves" : 20, "learning_rate" : 0.1, "bagging_fraction" : 0.8,
                'max_depth': 6}   
    lgb_model = lgb.train(params, train_ds, 1000, test_ds, verbose_eval=1000, early_stopping_rounds=100)
  * **RMSE score : 0.09477275477011567**   
     
* **function : price_pred(x1, x2,x3,x4, x5=77.95, x6=0,x7=0,x8=0,x9=9,x10=1998)**   
  * 'transaction_year' : x1, 'transaction_month' : x2, 'dong_enc' : x3, 'apt_name_enc' : x4, 'use_area(m2)' : x5, 'date(1\~10)' : x6, 'date(11\~20)' : x7, 'date(21~)' : x8, 'floor' : x9, 'year_found' : x10
## 2)아파트 주변 공원 시각화 모델    
![image](https://user-images.githubusercontent.com/67865191/107124336-b0a06300-68e6-11eb-9aec-3f675b9dd904.PNG)
* parkWithLatLng_after.csv : Selenium, chromedriver 이용하여 카카오맵에서 공원 이름으로 도로명 주소 크롤링 한 뒤, 카카오 지도api 이용하여 주소로 위도, 경도 값 추출   
  * 원래의 park.csv 데이터에서 'city'+'gu'+'dong'+'park_name'+'park_type'을 이용하여 정확한 도로명 주소를 크롤링 한 것이기 때문에 검색이 안되는 경우도 있었음, 'city'+'gu'+'dong'+'park_name' 으로 한번 더 크롤링 후 위의 경우에 겹쳐줌. -> 최종 결측치 166개   
* **function**
  * id(name) : 카카오지도api를 이용하여 사용자가 아파트 이름을 입력하면 자동으로 apt_address.csv에 있는 주소로 변환 후 위도와 경도 반환
  * get_close_index(apt_name) : haversine 라이브러리를 이용하여 입력한 아파트의 위도, 경도와 모든 공원들의 위도, 경도간 거리를 계산 후 500m 이하의 공원 인덱스를 반환해줌
  * get_map(address) : 위의 함수들을 이용하여 최종적으로 밑과 같은 plotly를 활용한 시각화 지도를 반환해줌
![image](https://user-images.githubusercontent.com/67865191/107124798-4210d480-68e9-11eb-9069-e456cf3efa7d.PNG)
* time function으로 재본 주소 입력부터 지도 시각화가 뜨기까지의 평균 시간 **약 15초**
# Backend Process

![image](https://user-images.githubusercontent.com/61021101/106378904-98fb4300-63eb-11eb-9d4f-0d1c3be15d13.png)

# Frontend Process

![image](https://user-images.githubusercontent.com/61021101/106378946-d790fd80-63eb-11eb-8be6-7c44502134d7.png)

# Result
![image](https://user-images.githubusercontent.com/61021101/106378988-2048b680-63ec-11eb-893d-4bca470a1197.png)

# Reference

