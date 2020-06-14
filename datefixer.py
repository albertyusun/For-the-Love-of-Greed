import pandas as pd

# find the first string of numbers, of length 4, beginning with a 1. that's the year.
# this function goes into publication string and finds the year date embedded in there.
# some dates replace the last digit with ?, indicating the precise year is unknown, but the decade
# is known. this code guesses the year to be halfway through the decade.
# also, some dates have a ? after the date, indicating the year is uncertain. there's not much we can
# do to deal with this, so this code just grabs the guess provided.
# also, some dates are written like 1.5.4.6. this code deals with that, though it does not accept
# dates written like 1.546 or 15.4.6.
# finally, sometimes there are multiple possible years listed. this code grabs the first year given.

# give it a publication entry. it gives you a year (as string).

def findDate(search):
    year = "????"
    for j in range(len(search)):
        if search[j] == "1":
            if search[j + 1] in int_list:
                if search[j + 2] in int_list:
                    if search[j + 3] in int_list:
                        print(search[j:j + 4])
                        year = search[j:j + 4]
                        return year
                    elif search[j + 3] == "?":
                        print(search[j:j + 4])
                        year = search[j:j + 3] + "5"
                        return year
            elif search[j + 1] == ".":
                if search[j + 2] in int_list:
                    if search[j + 3] == ".":
                        if search[j + 4] in int_list:
                            if search[j + 5] == ".":
                                if search[j + 6] in int_list:
                                    print(search[j] + search[j + 2] + search[j + 4] + search[j + 6])
                                    year = search[j] + search[j + 2] + search[j + 4] + search[j + 6]
                                    return year
    return year

df = pd.read_csv("CSVs/dirtydata_TCP_1_1.csv")

pubinfo = df["publishinfo"].tolist()
dates = df["dates"].tolist()
print(dates)

int_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

# we only want to change the dates for the entries where the date is in error.

for i in range(len(pubinfo)):
    if findDate(pubinfo[i]) != dates[i]:
        dates[i] = findDate(pubinfo[i])

print(dates)
df["dates"] = dates

df.to_csv("testdirtydata1.csv")