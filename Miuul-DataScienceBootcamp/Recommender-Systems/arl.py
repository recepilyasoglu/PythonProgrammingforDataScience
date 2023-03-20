############################################
# ASSOCIATION RULE LEARNING (BİRLİKTELİK KURALI ÖĞRENİMİ)
############################################

# 1. Veri Ön İşleme
# 2. ARL Veri Yapısını Hazırlama (Invoice-Product Matrix)
# 3. Birliktelik Kurallarının Çıkarılması
# 4. Çalışmanın Scriptini Hazırlama
# 5. Sepet Aşamasındaki Kullanıcılara Ürün Önerisinde Bulunmak

############################################
# 1. Veri Ön İşleme
############################################

# !pip install mlxtend
import pandas as pd

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
# çıktının tek bir satırda olmasını sağlar.
pd.set_option('display.expand_frame_repr', False)
from mlxtend.frequent_patterns import apriori, association_rules

df_ = pd.read_excel("Recommender-Systems/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()
df.head()

df.describe().T  # eksi değerler var olmaması lazım, ve aykırı değerler var çeyrekliklere bakılınca anlaşılıyor
df.isnull().sum()
df.shape


def retail_data_prep(dataframe):
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    return dataframe


df = retail_data_prep(df)


# ilk olarak, girilen değişkenin %1 çeyrek değerini ve %99 çeyrek değerini hesaplayıp değişkenler de bunu bir tut,
# sonra diyoruz ki %99 luk çeyrek  değerden 1,5 IQR uzaklıktaki değer benim üst limitimdir,
# %1 lik çeyrek  değerden 1,5 IQR yakınındaki değer benim alt limitimdir.
def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit


# yukarıda hesaplanan değere göre baskılama yapmak
# ilgili değişkenden küçük olanlar var mı bak, yukarıda belirlenen low limitten küçük ve ilgili değişkeni, low limite tekrar ata yani baskıla
# aynı şeyi up limit için de yap
def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


# yeniden çağırıp yukarıdaki fonksiyonları da ekliyoruz bu sefer
def retail_data_prep(dataframe):
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    replace_with_thresholds(dataframe, "Quantity")
    replace_with_thresholds(dataframe, "Price")
    return dataframe


df = retail_data_prep(df)
df.isnull().sum()
df.describe().T

#########################################################
# 2. ARL Veri Yapısını Hazırlama (Invoice-Product Matrix)
#########################################################
# Genel Amaç= Product Matrix, her bir faturaya ait ürünler(description), sütunlarda yazacak ve o fatura da o ürün varsa 1 yoksa 0
df.head()

df_fr = df[df["Country"] == "France"]
df_fr.head()

df.groupby(["Invoice", "Description"]).agg({"Quantity": "sum"}).head(20)

# Description'ları sütuna geçirmek için
# unstack() diyerek pivot yapıyoruz, sonra da satır ve sütunlardan 5'er tane getir
df.groupby(["Invoice", "Description"]).agg({"Quantity": "sum"}).unstack().iloc[0:5, 0:5]

# unstack den sonra NAN olan yerleri 0 ile doldurma
df.groupby(["Invoice", "Description"]).agg({"Quantity": "sum"}).unstack().fillna(0).iloc[0:5, 0:5]

# applaymap ile olan ürünlere 1 olmayanlara 0 yazdırma
df.groupby(["Invoice", "StockCode"]). \
    agg({"Quantity": "sum"}). \
    unstack(). \
    fillna(0). \
    applymap(lambda x: 1 if x > 0 else 0).iloc[0:5, 0:5]


# id = True olursa yani girilirse yukarıda yapılan işi StockCode'a göre yap
def create_invoice_product_df(dataframe, id=False):
    if id:
        return dataframe.groupby(["Invoice", "StockCode"])["Quantity"].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)
    else:
        return dataframe.groupby(["Invoice", "Description"])["Quantity"].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)

fr_inv_pro_df = create_invoice_product_df(df_fr)

fr_inv_pro_df = create_invoice_product_df(df_fr, id=True)


# verilen id'ye göre ürün bulma
def check_id(dataframe, stock_code):
    product_name = dataframe[dataframe["StockCode"] == stock_code][["Description"]].values[0].tolist()
    print(product_name)

check_id(df_fr, 10002)
check_id(df_fr, 10120)
