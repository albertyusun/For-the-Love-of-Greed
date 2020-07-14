import pandas as pd
import re

date_buckets = ["1470-1494", "1495-1519", "1520-1544", "1545-1569", "1570-1594",
                "1595-1619", "1620-1644", "1645-1669", "1670-1700"]


# structural garbage
pageA = re.compile('Page Â')
pageUn1 = re.compile(r'Page  \[unnumbered\]')
pageUn2 = re.compile(r'Page \[unnumbered\]')
PageNum = re.compile(r'Page  [0123456789]')
pageNum = re.compile(r'page  [0123456789]')
Un = re.compile(r'\[unnumbered\]')
illust = re.compile(r'\[illustration\]')
Illust = re.compile(r'\[Illustration\]')
Chapter = re.compile('Chapter [0123456789]')
chapter = re.compile('chapter [0123456789]')
Chapt1 = re.compile(r'Chapt\. [0123456789]')
chapt1 = re.compile(r'chapt\. [0123456789]')
Chapt = re.compile('Chapt [0123456789]')
chapt = re.compile('chapt [0123456789]')
structural_garbage = [pageA, pageUn1, pageUn2, PageNum, pageNum, Un, illust, Illust, Chapter, chapter,
                      Chapt1, chapt1, Chapt, chapt]

# some punctuation
amper = re.compile('&')
dash = re.compile('—')

# etc.
etc = re.compile('andc')

# text accents
above = re.compile('̄')
a = re.compile('[àáâãäå]')
A = re.compile('[ÀÁÂÃÄÅ]')
e = re.compile('[ęèéêë]')
E = re.compile('[ÈÉÊË]')
ii = re.compile('[ìíîï]')
II = re.compile('[ÌÍÎÏ]')
o = re.compile('[òóôõö]')
O = re.compile('[ÒÓÔÕÖ]')
u = re.compile('[ùúûü]')
U = re.compile('[ÙÚÛÜ]')
c = re.compile('ç')
C = re.compile('Ç')
ae = re.compile('æ')
AE = re.compile('Æ')
oe = re.compile('œ')
thorn = re.compile('[þÞ]')
B = re.compile('ß')

# finally, everything else (except hyphens and apostrophes)
everything = re.compile(r"[^a-zA-Z'\- ]")

# then, attempt to get rid of roman numerals (except those containing exactly one I)
roman = re.compile(r"\b((?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?(I{0}|I{2,})))\b",
                   re.IGNORECASE)

# finally, remove extra spaces
spaces = re.compile(r" {2,}")


def clean_text():
    for date in date_buckets:
        df = pd.read_csv("CSVs/"+date+"dirty.csv")
        texts = df['booktext'].tolist()

        for i in range(len(texts)):
            temp = texts[i]

            # remove structural garbage
            for trash in structural_garbage:
                temp = trash.sub("", temp)

            # replace & with and, and the em-dash with a space
            temp = amper.sub("and", temp)
            temp = dash.sub(" ", temp)

            # delete weird above symbol, replace some utf-8 variants with normal letters.
            temp = above.sub("", temp)
            temp = a.sub("a", temp)
            temp = A.sub("A", temp)
            temp = e.sub("e", temp)
            temp = E.sub("E", temp)
            temp = ii.sub("i", temp)
            temp = II.sub("I", temp)
            temp = o.sub("o", temp)
            temp = O.sub("O", temp)
            temp = u.sub("u", temp)
            temp = U.sub("U", temp)
            temp = c.sub("c", temp)
            temp = C.sub("C", temp)
            temp = ae.sub("ae", temp)
            temp = AE.sub("AE", temp)
            temp = oe.sub("oe", temp)
            temp = thorn.sub("th", temp)
            temp = B.sub("B", temp)

            # remove everything else, except for hyphens, apostrophes, letters, and spaces
            temp = everything.sub("", temp)

            # replace 'andc' artifact with &c
            # delete roman numerals (except for I)
            temp = etc.sub("&c", temp)
            temp = roman.sub("", temp)
            temp = spaces.sub(" ", temp)

            # lowercase temp, then upload it
            temp = temp.lower()
            texts[i] = temp

        df['booktext'] = texts
        print(date, "cleaned")
        df.to_csv("CSVs/"+date+"clean.csv")


# replaces variant spellings with the base word
def sub_variants():
    for date in date_buckets:
        df = pd.read_csv("CSVs/spellingvariations/wordVariation"+date+".csv")
        DF = pd.read_csv("CSVs/"+date+"clean.csv")
        texts = DF["booktext"].tolist()
        base_words = []
        columns = []

        # get principal words and stored column names for simplicity
        for col in df.columns:
            columns.append(col)
            base_words.append(col[4:].lower())
        print("finished fetching base words")

        # initialize variants dictionary
        variants = {}
        for word in base_words:
            variants[word] = []
        print("variants initialized")

        # store regex's of each variant
        for i in range(len(columns)):
            for variant in df[columns[i]]:
                if type(variant) is str:
                    variants[base_words[i]].append(re.compile("\\b"+variant+"\\b"))
        print("finished fetching spelling variants")

        # now replace each dictionary value in variants with its key
        for j in range(len(texts)):
            temp = texts[j]
            for word in base_words:
                for var in variants[word]:
                    temp = var.sub(word, temp)
            texts[j] = temp
        DF["booktext"] = texts
        DF.to_csv("CSVs/"+date+"cleansub.csv")
        print("finished replacing variants for", date)


sub_variants()
