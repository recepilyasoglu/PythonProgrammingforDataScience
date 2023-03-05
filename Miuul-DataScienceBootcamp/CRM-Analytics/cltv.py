#######################################################
# CUSTOMER LIFETIME VALUE (Müşteri Yaşam Boyu Değeri) #
#######################################################

# 1. Veri Hazırlama
# 2. Average Order Value (Total Price / Total Transaction)
# 3. Purchase Frequency (Total Transaction / Total Number of Customers)
# 4. Repeat Rate & Churn Rate (Birden fazla alışveriş yapan müşteriler sayısı / tüm müşteriler)
# 5. Profit Margin = Total Price * 0.10
# 6. Customer Value = Average Order Value * Purchase Frequency
# 7. CLTV = (Customer Value / Churn Rate) x Profit Margin
# 8. Segmentlerin Oluşturulması
# 9. BONUS: Tüm İşlemlerin Fonksiyonlaştırılması


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
from sklearn.preprocessing import MinMaxScaler
pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)  # 0 dan sonra kaç basamak okuyacağını belirleme

df_ = pd.read_excel(r"CRM-Analytics/datasets/online_retail_II.xlsx", sheet_name="Year 2009-2010")
df = df_.copy()
df.head()










