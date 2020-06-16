import pandas as pd

date_buckets = ["1470-1479","1480-1489", "1490-1499", "1500-1509", "1510-1519", "1520-1529", "1530-1539",
                "1540-1549", "1550-1559", "1560-1569", "1570-1579", "1580-1589", "1590-1599", "1600-1609",
                "1610-1619", "1620-1629", "1630-1639", "1640-1649", "1650-1659", "1660-1669", "1670-1679",
                "1680-1689", "1690-1700"]  # these are all inclusive buckets

# dataframe buckets
listInList = [["website", "title", "author", "publishinfo", "dates", "booktext"]]

df1 = pd.DataFrame(listInList[1:], columns=listInList[0])
df2 = pd.DataFrame(listInList[1:], columns=listInList[0])
df3 = pd.DataFrame(listInList[1:], columns=listInList[0])
df4 = pd.DataFrame(listInList[1:], columns=listInList[0])
df5 = pd.DataFrame(listInList[1:], columns=listInList[0])
df6 = pd.DataFrame(listInList[1:], columns=listInList[0])
df7 = pd.DataFrame(listInList[1:], columns=listInList[0])
df8 = pd.DataFrame(listInList[1:], columns=listInList[0])
df9 = pd.DataFrame(listInList[1:], columns=listInList[0])
df10 = pd.DataFrame(listInList[1:], columns=listInList[0])
df11 = pd.DataFrame(listInList[1:], columns=listInList[0])
df12 = pd.DataFrame(listInList[1:], columns=listInList[0])
df13 = pd.DataFrame(listInList[1:], columns=listInList[0])
df14 = pd.DataFrame(listInList[1:], columns=listInList[0])
df15 = pd.DataFrame(listInList[1:], columns=listInList[0])
df16 = pd.DataFrame(listInList[1:], columns=listInList[0])
df17 = pd.DataFrame(listInList[1:], columns=listInList[0])
df18 = pd.DataFrame(listInList[1:], columns=listInList[0])
df19 = pd.DataFrame(listInList[1:], columns=listInList[0])
df20 = pd.DataFrame(listInList[1:], columns=listInList[0])
df21 = pd.DataFrame(listInList[1:], columns=listInList[0])
df22 = pd.DataFrame(listInList[1:], columns=listInList[0])
df23 = pd.DataFrame(listInList[1:], columns=listInList[0])

prefix = "data_TCP_1_"

count = 1
while count < 26:  # there are 25 csv files
    df = pd.read_csv("CSVs/"+prefix+str(count)+".csv")
    indexing = df["Unnamed: 0"].tolist()

    for i in indexing:
        if df.at[i, "dates"] != "????":
            if 1470 <= int(df.at[i, "dates"]) <= 1479:
                df1 = df1.append(df.iloc[i])
            elif 1480 <= int(df.at[i, "dates"]) <= 1489:
                df2 = df2.append(df.iloc[i])
            elif 1490 <= int(df.at[i, "dates"]) <= 1499:
                df3 = df3.append(df.iloc[i])
            elif 1500 <= int(df.at[i, "dates"]) <= 1509:
                df4 = df4.append(df.iloc[i])
            elif 1510 <= int(df.at[i, "dates"]) <= 1519:
                df5 = df5.append(df.iloc[i])
            elif 1520 <= int(df.at[i, "dates"]) <= 1529:
                df6 = df6.append(df.iloc[i])
            elif 1530 <= int(df.at[i, "dates"]) <= 1539:
                df7 = df7.append(df.iloc[i])
            elif 1540 <= int(df.at[i, "dates"]) <= 1549:
                df8 = df8.append(df.iloc[i])
            elif 1550 <= int(df.at[i, "dates"]) <= 1559:
                df9 = df9.append(df.iloc[i])
            elif 1560 <= int(df.at[i, "dates"]) <= 1569:
                df10 = df10.append(df.iloc[i])
            elif 1570 <= int(df.at[i, "dates"]) <= 1579:
                df11 = df11.append(df.iloc[i])
            elif 1580 <= int(df.at[i, "dates"]) <= 1589:
                df12 = df12.append(df.iloc[i])
            elif 1590 <= int(df.at[i, "dates"]) <= 1599:
                df13 = df13.append(df.iloc[i])
            elif 1600 <= int(df.at[i, "dates"]) <= 1609:
                df14 = df14.append(df.iloc[i])
            elif 1610 <= int(df.at[i, "dates"]) <= 1619:
                df15 = df15.append(df.iloc[i])
            elif 1620 <= int(df.at[i, "dates"]) <= 1629:
                df16 = df16.append(df.iloc[i])
            elif 1630 <= int(df.at[i, "dates"]) <= 1639:
                df17 = df17.append(df.iloc[i])
            elif 1640 <= int(df.at[i, "dates"]) <= 1649:
                df18 = df18.append(df.iloc[i])
            elif 1650 <= int(df.at[i, "dates"]) <= 1659:
                df19 = df19.append(df.iloc[i])
            elif 1660 <= int(df.at[i, "dates"]) <= 1669:
                df20 = df20.append(df.iloc[i])
            elif 1670 <= int(df.at[i, "dates"]) <= 1679:
                df21 = df21.append(df.iloc[i])
            elif 1680 <= int(df.at[i, "dates"]) <= 1689:
                df22 = df22.append(df.iloc[i])
            elif 1690 <= int(df.at[i, "dates"]) <= 1700:
                df23 = df23.append(df.iloc[i])
    print(count)
    count += 1

df1.to_csv("CSVs/"+date_buckets[0]+".csv")
print("1 done")
df2.to_csv("CSVs/"+date_buckets[1]+".csv")
print("2 done")
df3.to_csv("CSVs/"+date_buckets[2]+".csv")
print("3 done")
df4.to_csv("CSVs/"+date_buckets[3]+".csv")
print("4 done")
df5.to_csv("CSVs/"+date_buckets[4]+".csv")
print("5 done")
df6.to_csv("CSVs/"+date_buckets[5]+".csv")
print("6 done")
df7.to_csv("CSVs/"+date_buckets[6]+".csv")
print("7 done")
df8.to_csv("CSVs/"+date_buckets[7]+".csv")
print("8 done")
df9.to_csv("CSVs/"+date_buckets[8]+".csv")
print("9 done")
df10.to_csv("CSVs/"+date_buckets[9]+".csv")
print("10 done")
df11.to_csv("CSVs/"+date_buckets[10]+".csv")
print("11 done")
df12.to_csv("CSVs/"+date_buckets[11]+".csv")
print("12 done")
df13.to_csv("CSVs/"+date_buckets[12]+".csv")
print("13 done")
df14.to_csv("CSVs/"+date_buckets[13]+".csv")
print("14 done")
df15.to_csv("CSVs/"+date_buckets[14]+".csv")
print("15 done")
df16.to_csv("CSVs/"+date_buckets[15]+".csv")
print("16 done")
df17.to_csv("CSVs/"+date_buckets[16]+".csv")
print("17 done")
df18.to_csv("CSVs/"+date_buckets[17]+".csv")
print("18 done")
df19.to_csv("CSVs/"+date_buckets[18]+".csv")
print("19 done")
df20.to_csv("CSVs/"+date_buckets[19]+".csv")
print("20 done")
df21.to_csv("CSVs/"+date_buckets[20]+".csv")
print("21 done")
df22.to_csv("CSVs/"+date_buckets[21]+".csv")
print("22 done")
df23.to_csv("CSVs/"+date_buckets[22]+".csv")
print("23 done")
