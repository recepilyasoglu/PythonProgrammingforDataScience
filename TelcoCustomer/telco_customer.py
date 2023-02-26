# 1- Import the required libraries. And then Telco Cutomer Read the Churn dataset
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv("Telco-Customer-Churn.csv")
df = data.copy()
df.head()


# 2- Telco Customer Churn data set;
# • Shape
# • Dtypes
# • Head, Tail
# • Missing Value
# • Describe
# obtain information.

df.shape
df.dtypes
df.head()
df.tail()
df.isnull().sum()
df.describe().T


# 3-Navigating in the Gender column of the dataset and "Male" of the gender column
# It prints 0 when it encounters the class, 1 when it encounters the opposite situation.
# Type comphrension and create a new file named "num_gender". assign to variable

#def check_gender(gender):
#        if gender == "Male":
#            return 0
#        else:
#            return 1

#df["num_gender"] = df["gender"].apply(lambda x: check_gender(x))

df["num_gender"] = [0 if col == "Male" else 1 for col in df.gender]


# 4- For the "Yes" class within the classes of the "PaperlessBilling" column
# Write a lambda function that prints "Yes" , "No" otherwise. And
# put the result in your newly created column named "NEW_PaperlessBilling"
# print it. (you can use lambda function with apply)

df["NEW_PaperlessBilling"] = df["PaperlessBilling"].apply(lambda x: "Evt" if x == "Yes" else "Hyr")


# 5- Those whose class is "Yes" within the scope of columns containing "Online" in the data set, "Yes", "No"
# Write code that will reformat the classes as "No", otherwise "No_Internet".
# Note: In order not to encounter if elif else syntax error in lambda, use another def function.
# Repeat classes as "Yes" for "yes", "No" for "No", otherwise "No_Internet".
# You can create the function to format it outside and apply this function inside the lambda.

def check_online(col):
        if col == "Yes":
           return "Evet"
        elif col == "No":
           return "Hayır"
        else:
           return "Interneti_yok"

online = df.filter(like="Online")
#online.head(25)
for col in online:
    df[col] = df[col].apply(lambda x: check_online(x))

df.filter(like="Online").head(25)


# 6- Find the values of "TotalCharges" variable less than 30. If
# If you get an error, examine the type of observations of this variable and
# to the query by converting it to the appropriate type for the specified query to arrive.
# continue

df["TotalCharges"].dtypes