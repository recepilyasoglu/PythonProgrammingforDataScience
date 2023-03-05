#############################################
# BG-NBD ve Gamma-Gamma ile CLTV Prediction #
#############################################

# 1. Data Preparation (Verinin Hazırlanması)
# 2. BG-NBD Modeli ile Expected Number of Transaction
# 3. Gamma-Gamma Modeli ile Expected Average Profit
# 4. BG-NBD ve Gamma-Gamma Modeli ile CLTV'nin Hesaplanması
# 5. CLTV'ye Göre Segmentleri Oluşturulması
# 6. Çalışmanın Fonksiyonlaştırılması


## 1. Veri Hazırlama

## Değişkenler
# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numaraç C ile başlıyorsa iptal edilen işlem
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihih ve zamanı
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz Müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke

import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 500)
pd.set_option('display.float_format', lambda x: '%.4f' % x)
from sklearn.preprocessing import MinMaxScaler


def outlier_thresholds(dataframe, variable):  # Amacı: kendisine girilen değişken için eşik değer belirlemektir
    quartile1 = dataframe[variable].quantile(0.01)  # quantile: çeyreklik hesaplama için
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def replace_with_threshold(dataframe, variable):  #
    low_limit, upl_limit = outlier_thresholds(dataframe, variable)
    # dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > upl_limit), variable] = upl_limit

df_ = pd.read_excel(r"CRM-Analytics/datasets/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()
df.head()
df.describe().T
df.isnull().sum()

# Veri Ön İşleme
df.dropna(inplace=True)
df = df[~df["Invoice"].str.contains("C", na=False)]  # iptal edilen ürünleri düşürme
df = df[(df["Quantity"] > 0)]
df = df[(df["Price"] > 0)]

# !!!!!!!!!!!!!!!!!!!!!!!!!
# içerisinde bildirdiğimiz yardımcı fonksiyonu çağıracak, Quantity değişkeni için eşik değerleri hesaplıcak
# daha sonra bu fonksiyonda o eşik değerlerin üzerinde kalan değerleri o eşik değerler ile değiştirecek
# !!!!!!!!!!!!!!!!!!!!!!!!!
replace_with_threshold(df, "Quantity")
replace_with_threshold(df, "Price")

df["TotalPrice"] = df["Quantity"] * df["Price"]

today_date = dt.datetime(2011, 12, 11)


## Preparation of Lifetime Data Structure (Lifetime Veri Yapısının Hazırlanması)

# recency: Son satın alma ğzerinden geçen zaman. Haftalık. (kullanıcı özelinde)
# T: Müşterinin yaşı. Haftalık (analiz tarihinden ne kadar süre önce ilk satın alma yapılmış)
# frequency: tekar eden toplan satın alma sayısı (frequency > 1)
# monetary: satın alma başına ortalama kazanç
# (Not: rfm'dekiler gibi değil)

cltv_df = df.groupby("Customer ID").agg({"InvoiceDate": [lambda InvoiceDate: (InvoiceDate.max() - InvoiceDate.min()).days,  # her bir müşterinin, son alışveriş ve ilk alışveriş tarihini birbirinden çıkar ve gün cinsine çevir
                                                         lambda date: (today_date - date.min()).days],  # müşterinin yaşını hesapla
                                         "Invoice": lambda Invoice: Invoice.nunique(),  # her bir müşterinin eşsiz kaç tane faturası var (=frequency)
                                         "TotalPrice": lambda TotalPrice: TotalPrice.sum()})

cltv_df.columns = cltv_df.columns.droplevel(0)

cltv_df.columns = ["recency", "T", "frequency", "monetary"]

cltv_df['monetary'] = cltv_df['monetary'] / cltv_df['frequency']

cltv_df.describe().T

cltv_df = cltv_df[(cltv_df["frequency"] > 1)]

# müşteri yaşı değerlerini haftalık cinsine çevirme
cltv_df["recency"] = cltv_df["recency"] / 7

cltv_df["T"] = cltv_df["T"] / 7
