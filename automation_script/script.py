import logging
import os
from datetime import datetime

#1. Create Logs folder if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

#2. Define log file name with timestamp
log_filename = datetime.now().strftime("logs/log_%Y-%m-%d_%H-%M-%S.log")

# 3. Configure logging
logging.basicConfig(
    filename=log_filename,            # Log file path
    filemode='w',                     # Overwrite each run; use 'a' for append
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    level=logging.DEBUG               # Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
)



#now automation script 

import pandas as pd
import numpy as np
import os
os.chdir("..")
vendor_invoice=pd.read_csv("data/vendor_invoice.csv")
sales=pd.read_csv("data/sales.csv")
purchases=pd.read_csv("data/purchases.csv")
purchase_prices=pd.read_csv("data/purchase_prices.csv")
begin_inventory=pd.read_csv("data/begin_inventory.csv")
end_inventory=pd.read_csv("data/end_inventory.csv")

logging.info("Files Read Sucessfully")
vi=vendor_invoice
s=sales
p=purchases
pp=purchase_prices

## now groupby the data for the reduce the complexity of the data and only taking the meanfully data with the low gradunality

s1=sales.groupby(["Brand","VendorNo"])[["SalesDollars","SalesQuantity","ExciseTax"]].sum().reset_index()
vi1=vi.groupby(["VendorNumber","VendorName"])[["Freight"]].sum().reset_index()
p1=p.groupby(["Brand","VendorNumber"])[["PurchasePrice","Quantity","Dollars"]].sum().reset_index()
pp1=pp.groupby(["Brand","VendorNumber","Description"])[["PurchasePrice","Price"]].sum().reset_index()
logging.info("Data tables has been aggreate for the reducing the complexity of the data")


#now joining the data data tables for the one final data 
#now join the tables
df1=p1.merge(s1,left_on=["Brand","VendorNumber"],right_on=["Brand","VendorNo"],how="left")
df2=df1.merge(vi1,left_on=["VendorNumber"],right_on="VendorNumber",how="left")
df=df2.merge(pp1,left_on=["VendorNumber","Brand"],right_on=["VendorNumber","Brand"],how="left")

data=df.rename(columns={"PurchasePrice_x":"TotalPurchasePrice",
                   "PurchasePrice_y":"PurchasePricePerUnit",
                   "Price":"ActualPricePerUnit",
                   "SalesQuantity":"TotalSalesQuantity",
                   "SalesDollars":"TotalSalesDollars",
                   "Dollars":"TotalPurchaseDollars",
                   "Quantity":"TotalPurchaseQuantity",
                      "Freight":"FreightCost",
                  })

logging.info("data has been  merge Successfully")



##Data preprocessing using the remove the duplicates,null values , format the data and save into the final and save data

#droping duplicates
data=data.drop_duplicates()
logging.info("duplicates has been drop successfully")

#remove the null 
data=data.dropna()
logging.info("null values  has been drop successfully")


#removing the extrawhite space from the data
data["VendorName"]=data["VendorName"].str.strip()
data["Description"]=data["Description"].str.strip()
logging.info("data cleaning has been  successfully")



## Now create the field which need for the further analysis
data["GrossProfit"]=data["TotalSalesDollars"]-data["TotalPurchaseDollars"]
data["ProfitMargin"]=round((data["GrossProfit"]/data["TotalSalesDollars"])*100,2)
data["StockTurnOver"]=round(data["TotalSalesQuantity"]/data["TotalPurchaseQuantity"],2)
data["SalesPurchaseRatio"]=round(data["TotalSalesDollars"]/data["TotalPurchaseDollars"],2)
logging.info("new data fields creation  has been  successfully")

#saving the data into the final table
data.to_csv("data/vendor_sales_data.csv")
logging.info("final data has been saved   successfully")






























