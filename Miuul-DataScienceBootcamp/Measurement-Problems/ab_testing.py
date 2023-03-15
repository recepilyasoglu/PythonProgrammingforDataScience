###############################
# Temel İstatistik Kavramları #
###############################

import itertools

import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Qt5Agg")
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
pd.set_option("display.width", 500)

# Sampling (Örnekleme)
populasyon = np.random.randint(0, 80, 10000)
populasyon.mean()

np.random.seed(115)

orneklem = np.random.choice(a=populasyon, size=100)
orneklem.mean()

np.random.seed(10)
orneklem1 = np.random.choice(a=populasyon, size=100)
orneklem2 = np.random.choice(a=populasyon, size=100)
orneklem3 = np.random.choice(a=populasyon, size=100)
orneklem4 = np.random.choice(a=populasyon, size=100)
orneklem5 = np.random.choice(a=populasyon, size=100)
orneklem6 = np.random.choice(a=populasyon, size=100)
orneklem7 = np.random.choice(a=populasyon, size=100)
orneklem8 = np.random.choice(a=populasyon, size=100)
orneklem9 = np.random.choice(a=populasyon, size=100)
orneklem10 = np.random.choice(a=populasyon, size=100)

(orneklem1.mean() + orneklem2.mean() + orneklem3.mean() + orneklem4.mean() + orneklem5.mean() + \
 orneklem6.mean() + orneklem7.mean() + orneklem8.mean() + orneklem9.mean() + orneklem10.mean()) / 10


# Descriptive Statistics (Betimsel İstatistikler)
df = sns.load_dataset("tips")
df.describe().T


# Confidence Intervals (Güven Aralıkları)
df = sns.load_dataset("tips")
df.describe().T

df.head()

# TotalBill değişkeninin güven aralığı nedir?
sms.DescrStatsW(df["total_bill"]).tconfint_mean()
# tip değişkeninin güven aralığı nedir?
sms.DescrStatsW(df["tip"]).tconfint_mean()

# Titanic Veri Setindeki Sayısal Değişkenler için Güven Aralığı
df = sns.load_dataset("titanic")
df.describe().T
sms.DescrStatsW(df["age"].dropna()).tconfint_mean()

sms.DescrStatsW(df["fare"].dropna()).tconfint_mean()


# Correlation (Korelasyon)

# Bahşiş veri seti:
# total_bill: yemeğin toplam fiyatı (bahşiş ve vergi dahil)
# tip: bahşiş
# sex: ücreti ödeyen kişinin cinsiyeti (0=male, 1=female)
# smoker: grupta sigara içen var mı? (0=No, 1=Yes)
# day: gün (3=Thur, 4=Fri, 5=Sat, 6=Sun)
# time: ne zaman? (0=Day, 1=Night)
# size: grupta kaç kişi var?

df = sns.load_dataset("tips")
df.head()

# Verilen Bahşişler ile Ödenen Hesap arasındaki korelasyon var mı ?
df["total_bill"] = df["total_bill"] - df["tip"]

df.plot.scatter("tip", 'total_bill')
plt.show()

df["tip"].corr(df["total_bill"])  # Yorum: Pozitif yönlü orta şiddetli bir ilişki vardır.


# AB Testing (Bağımsız İki Örneklem T Testi)

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı
#   - 2. Varyans Homojenliği
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.


# Uygulama 1: Sigara İçenler ile İçmeyenlerin Hesap Ortalamaları Arasında İst Ol An Fark var mı?

df = sns.load_dataset("tips")
df.head()

df.groupby("smoker").agg({"total_bill": "mean"})


# 1. Hipotezi Kur
# H0: M1=M2
# H1 = M1 != M2


# 2. Varsayım Kontrolü

# Normallik Varsayımı
# Varyans Homojenliği


## Normallik Varsayımı

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: ...sağlanmamaktadır.

# shapiro testi bir değişkenin dağılımının normal olup olmadığını test eder.
test_stat, pvalue = shapiro(df.loc[df["smoker"] == "Yes", "total_bill"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

# p-value < ise 0.05'ten H0 RED.
# p-value < değilse 0.05 H0 REDDEILEMEZ.

test_stat, pvalue = shapiro(df.loc[df["smoker"] == "No", "total_bill"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))


## Varyans Homjenliği Varsayımı

# H0: Varyanslar Homojendir.
# H1: Varyanslar Homojen Değildir..

# levene: bana ik farlı grup gönder, bu iki farkli gruba göre bize
# varyans homojenliği varsayımının sağlanıp sağlanmadığını ifade eder.
test_stat, pvalue = levene(df.loc[df["smoker"] == "Yes", "total_bill"],
                           df.loc[df["smoker"] == "No", "total_bill"])

print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

# p-value < ise 0.05'ten H0 RED.
# p-value < değilse 0.05 H0 REDDEILEMEZ.


# 3. ve 4. Hipotezin Uygulanması

## 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
## 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)


## 1.1 Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)

# ttest: normallik varsayımı sağlanıyorsa kullanılır
# normallik varsayımı sağlanıyor ve varyans homojenliği varsayımı sağlanılıyorsa da kullanılır
# normallik varsayımı sağlanıyor ve varyans homojenliği varsayımı sağlanmıyorsa da kullanılır,
# sadece equal_var=False gir der

test_stat, pvalue = ttest_ind(df.loc[df["smoker"] == "Yes", "total_bill"],
                              df.loc[df["smoker"] == "No", "total_bill"],
                              equal_var=True)

print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

# p-value < ise 0.05'ten H0 RED.
# p-value < değilse 0.05 H0 REDDEILEMEZ.


# 1.2 Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)
# mannwhitneyu testi: non-parametrik ortalama/medyan kıyaslama testidir.

test_stat, pvalue = mannwhitneyu(df.loc[df["smoker"] == "Yes", "total_bill"],
                                 df.loc[df["smoker"] == "No", "total_bill"])

print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))


### Sonuç: H0 REDDEDILEMEZ ÇIKTI.
#Yani sigara içenler ile içmeyenler arasında fark yoktur.


# NOT:
# H0 ya reddedilir ya reddedilemez !!!
# H1'i kabul etmek diye br durum YOK !!!


# Uygulama 2: Titanic Kadın ve Erkek Yolcuların Yaş Ortalamaları Arasında İstatistiksel Olarak Anl. Fark. var mıdır?

df = sns.load_dataset("titanic")
df.head()

df.groupby("sex").agg({"age": "mean"})


# 1. Hipotezleri kur:
# H0: M1  = M2 (Kadın ve Erkek Yolcuların Yaş Ortalamaları Arasında İstatistiksel Olarak Anl. Fark. Yoktur)
# H1: M1! = M2 (... vardır)


# 2. Varsayımları İncele

# Normallik varsayımı
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır

test_stat, pvalue = shapiro(df.loc[df["sex"] == "female", "age"].dropna())
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

test_stat, pvalue = shapiro(df.loc[df["sex"] == "male", "age"].dropna())
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))


# Varyans homojenliği
# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene(df.loc[df["sex"] == "female", "age"].dropna(),
                           df.loc[df["sex"] == "male", "age"].dropna())

print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

# Varsayımlar sağlanmadığı için nonparametrik

test_stat, pvalue = mannwhitneyu(df.loc[df["sex"] == "female", "age"].dropna(),
                                 df.loc[df["sex"] == "male", "age"].dropna())

print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))


# Uygulama 3: Diyabet Hastası Olan ve Olmayanların Yaşları Ort. Arasında İst. Ol. Anl. Fark var mıdır?

df = pd.read_csv("Measurement-Problems/diabetes.csv")
df.head()

df.groupby("Outcome").agg({"Age": "mean"})

# 1. Hipotezleri kur
# H0: M1 = M2
# Diyabet Hastası Olan ve Olmayanların Yaşları Ort. Arasında İst. Ol. Anl. Fark Yoktur
# H1: M1 != M2
# .... vardır.

# 2. Varsayımları İncele

# Normallik Varsayımı (H0: Normal dağılım varsayımı sağlanmaktadır.)

test_stat, pvalue = shapiro(df.loc[df["Outcome"] == 1, "Age"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df.loc[df["Outcome"] == 0, "Age"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


# Normallik varsayımı sağlanmadığı için nonparametrik.

# Hipotez (H0: M1 = M2)
test_stat, pvalue = mannwhitneyu(df.loc[df["Outcome"] == 1, "Age"].dropna(),
                                 df.loc[df["Outcome"] == 0, "Age"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Sonuç: Yaşı daha büyük olanlar diyabet hastalığına yakalana ihtimali vardır denebilir.


# İş Problemi: Kursun Büyük Çoğunluğunu İzleyenler ile İzlemeyenlerin Puanları Birbirinden Farklı mı?
###################################################

# H0: M1 = M2 (... iki grup ortalamaları arasında ist ol.anl.fark yoktur.)
# H1: M1 != M2 (...vardır)

df = pd.read_csv("Measurement-Problems/course_reviews.csv")
df.head()

df[(df["Progress"] > 75)]["Rating"].mean()

df[(df["Progress"] < 10)]["Rating"].mean()

test_stat, pvalue = shapiro(df[(df["Progress"] > 75)]["Rating"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df[(df["Progress"] < 25)]["Rating"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = mannwhitneyu(df[(df["Progress"] > 75)]["Rating"],
                                 df[(df["Progress"] < 25)]["Rating"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


######################################################
# AB Testing (İki Örneklem Oran Testi)
######################################################

# H0: p1 = p2
# Yeni Tasarımın Dönüşüm Oranı ile Eski Tasarımın Dönüşüm Oranı Arasında İst. Ol. Anlamlı Farklılık Yoktur.
# H1: p1 != p2
# ... vardır

basari_sayisi = np.array([300, 250])
gozlem_sayilari = np.array([1000, 1100])

proportions_ztest(count=basari_sayisi, nobs=gozlem_sayilari)


basari_sayisi / gozlem_sayilari


############################
# Uygulama: Kadın ve Erkeklerin Hayatta Kalma Oranları Arasında İst. Olarak An. Farklılık var mıdır?
############################

# H0: p1 = p2
# Kadın ve Erkeklerin Hayatta Kalma Oranları Arasında İst. Olarak An. Fark yoktur

# H1: p1 != p2
# .. vardır

df = sns.load_dataset("titanic")
df.head()

df.loc[df["sex"] == "female", "survived"].mean()

df.loc[df["sex"] == "male", "survived"].mean()

female_succ_count = df.loc[df["sex"] == "female", "survived"].sum()
male_succ_count = df.loc[df["sex"] == "male", "survived"].sum()

test_stat, pvalue = proportions_ztest(count=[female_succ_count, male_succ_count],
                                      nobs=[df.loc[df["sex"] == "female", "survived"].shape[0],
                                            df.loc[df["sex"] == "male", "survived"].shape[0]])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))






