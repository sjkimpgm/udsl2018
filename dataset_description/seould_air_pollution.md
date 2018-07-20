## Data Schema

Order|Name|Description|Type
:--:|--|--|--
0|timestamp|measured timestamp|timestamp<br>(yyyy-MM-dd hh:mm:ss)
1|area_code|ID of measured district|unsigned int
2|pm10_value|PM10 concentration ($\mu g/m^3$)|float
3|pm2_5_value|PM2.5 concentration ($\mu g/m^3$)|float
4|o3|Ozone contenration ($ppm$)|float
5|no2|Nitrogen dioxide ($ppm$)|float
6|co|Carbon mono oxide ($ppm$)|float
7|so2|Sulful dioxide ($ppm$)|float
8|pm10_aqi|PM10 AQI|float
9|pm2_5_aqi|PM2.5 AQI|float
> pm10_value, pm2_5_value, pm10_aqi, pm2_5_aqi may be converted to unsigned int

### area_code
code|name|code|name
:--:|--|:--:|--
0|average|13|서대문구
1|종로구|14|마포구
2|중구|15|양천구
3|용산구|16|강서구
4|성동구|17|구로구
5|광진구|18|금천구
6|동대문구|19|영등포구
7|중랑구|20|동작구
8|성북구|21|관악구
9|강북구|22|서초구
10|도봉구|23|강남구
11|노원구|24|송파구
12|은평구|25|강동구

### AQI 계산 방법
$I_p  = (I_{HI}-I_{LO}) / (BP_{HI}-BP_{LO}) \times (C_p-BP_{LO}) + I_{LO}$

-   $I_p$  = 대상 오염물질의 대기지수점수
-   $C_p$  = 대상 오염물질의 대기 중 농도
-   $BP_{HI}$  = 대상 오염물질의 오염도 해당 구간에 대한 최대 오염도
-   $BP_{LO}$  = 대상 오염물질의 오염도 해당 구간에 대한 최소 오염도
-   $I_{HI}$  = $BP_{HI}$에 해당하는 지수값 (구간 최대 지수값)
-   $I_{LO}$  = $BP_{LO}$에 해당하는 지수값 (구간 최소 지수값)

지수|좋음|보통|나쁨|매우나쁨
:--:|--|--|--|--
AQI|0 ~ 50|51 ~ 100|101 ~ 250|251 ~
PM 2.5 ($\mu g/m^3$)|0 ~ 15|16 ~ 35|36 ~ 75|76 ~
PM 10 ($\mu g/m^3$)|0 ~ 30|31 ~ 80|81 ~ 150|151 ~
> reference; http://cleanair.seoul.go.kr/inform.htm?method=cai

ex> PM 2.5 = 18$\mu g/m^3$ 
PM2.5 AQI = $(100-51) / (35-16) \times (18-16) + 51 = 61$  (보통)

### Data Source
[서울특별시 대기환경정보](http://cleanair.seoul.go.kr/main.htm)
