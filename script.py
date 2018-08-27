import io
import re

stopwords = []
# ['już', 'podaje', 'to', 'bedzie', 'będzie', 'yyyy', 'hmmm', '', 'tak', 'em', 'no', 'znaczy', 'zatem', 'text', 'dobrze']

def date_recognition(text):
    day = 0
    month = 0
    year = 0

    regexp0 = ['zero',0]

    regexp1 = [
        ['pierwsz(y|ego)', 1],
        ['drugi(|ego)', 2],
        ['trzeci(|ego)', 3],
        ['czwart(y|ego)', 4],
        ['piąt(y|ego)', 5],
        ['szóst(y|ego)', 6],
        ['siódm(y|ego)', 7],
        ['ósm(y|ego)', 8],
        ['dziewiąt(y|ego)', 9]
    ]

    regexp2 = [
        ['dziesi(ęć|(ąt(y|ego)))', 10],
        ['jedena(ście|(st(y|ego)))', 11],
        ['dw(anaście|(unast(y|ego)))', 12],
        ['trzyna(ście|(st(y|ego)))', 13],
        ['czterna(ście|(st(y|ego)))', 14],
        ['piętna(ście|(st(y|ego)))', 15],
        ['szesna(ście|(st(y|ego)))', 16],
        ['siedemna(ście|(st(y|ego)))', 17],
        ['osiemna(ście|(st(y|ego)))', 18],
        ['dziewiętna(ście|(st(y|ego)))', 19]
    ]

    regexp3 = ['dwudziest(y|ego)', 20]

    regexp4 = [
        ['stycz(nia|eń)', 1],
        ['lut(ego|y)', 2],
        ['mar(zec|rca)', 3],
        ['kwie(cień|tnia)', 4],
        ['maj(|a)', 5],
        ['czerw(iec|ca)', 6],
        ['lip(iec|ca)', 7],
        ['sierp(ień|nia)', 8],
        ['wrześ(ień|nia)', 9],
        ['październik(|a)', 10],
        ['listopad(|a)', 11],
        ['grud(zień|nia)', 12]
    ]

    regexp5 = [
        ['dw(adzieścia|(udziest(y|ego)))', 20],
        ['trzydzie(ści|(st(y|ego)))', 30],
        ['czterdzie(ści|(st(y|ego)))', 40],
        ['pięćdziesiąt(y|ego)', 50],
        ['sześćdziesiąt(y|ego)', 60],
        ['siedemdziesiąt(y|ego)', 70],
        ['osiemdziesiąt(y|ego)', 80],
        ['dziewięćdziesiąt(y|ego)', 90]
    ]

    regexp6 = [
        ['jeden', 1],
        ['dwa', 2],
        ['trzy', 3],
        ['cztery', 4],
        ['pięć', 5],
        ['sześć', 6],
        ['siedem', 7],
        ['osiem', 8],
        ['dziewięć', 9]
    ]

    regexp7 = ['tysiąc(|e)', 1000]

    regexp8 = ['dwadzieścia', 20]


    matches = []

    z = re.finditer(regexp0[0], sentence)
    if z:
        for match in z:
            matches.append([match.start(), regexp0[1], 0])

    for i in range(len(regexp1)):
        z = re.finditer(regexp1[i][0], sentence)
        if z:
            for match in z:
                matches.append([match.start(), regexp1[i][1], 1])

    for i in range(len(regexp2)):
        z = re.finditer(regexp2[i][0], sentence)
        if z:
            for match in z:
                matches.append([match.start(), regexp2[i][1], 2])

    z = re.finditer(regexp3[0], sentence)
    if z:
        for match in z:
            matches.append([match.start(), regexp3[1], 3])

    for i in range(len(regexp4)):
        z = re.finditer(regexp4[i][0], sentence)
        if z:
            for match in z:
                matches.append([match.start(), regexp4[i][1], 4])

    for i in range(len(regexp5)):
        z = re.finditer(regexp5[i][0], sentence)
        if z:
            for match in z:
                matches.append([match.start(), regexp5[i][1], 5])

    for i in range(len(regexp6)):
        z = re.finditer(regexp6[i][0], sentence)
        if z:
            for match in z:
                matches.append([match.start(), regexp6[i][1], 6])

    z = re.finditer(regexp7[0], sentence)
    if z:
        for match in z:
                matches.append([match.start(), regexp7[1], 7])

    z = re.finditer(regexp8[0], sentence)
    if z:
        for match in z:
                matches.append([match.start(), regexp8[1], 8])


    sorted_matched = sorted(matches, key =lambda l:l[0], reverse = False)

    iter = 0
    day_trigger = True
    month_trigger = True
    year_trigger1 = True
    year_trigger2 = True
    position = -1
    temp = 0

    for it in range(len(sorted_matched)):
        if position == sorted_matched[it][0]:
            continue

        if sorted_matched[it][2] <= 2 and day_trigger:
            day = sorted_matched[it][1]
            # print(day)
            iter = it + 1
            day_trigger = False
            position = sorted_matched[it][0]
        elif sorted_matched[it][2] == 5 and day_trigger:
            day = sorted_matched[it][1] + sorted_matched[it+1][1]
            iter = it + 2
            day_trigger = False
            position = sorted_matched[it+1][0]

        elif sorted_matched[it][2] == 0 and it >= iter and not day_trigger and month_trigger:
            month = sorted_matched[it+1][1]
            iter = it+1
            month_trigger = False
            position = sorted_matched[it+1][0]
        elif sorted_matched[it][2] in [1,2,4,6] and not day_trigger and month_trigger:
            month = sorted_matched[it][1]
            iter = it+1
            month_trigger = False
            position = sorted_matched[it][0]
            # print(month)
        elif not day_trigger and not month_trigger:
            year_list = sorted_matched[it:]

            pos = 0

            if year_list[0][2] == 2 or year_list[0][2] == 7 and year_trigger1:
                temp = 1900
                year_trigger1 = False
                pos = 1
            elif year_list[0][2] == 5 or (year_list[0][2] == 6 and year_list[1][2] == 7) and year_trigger1:
                temp = 2000
                year_trigger1 = False
                if year_list[0][2] == 5:
                    pos = 1
                elif year_list[0][2] == 6 and year_list[1][2] == 7:
                    pos = 2

            if not year_trigger1 and year_trigger2:
                if year_list[-2][2] == 5:
                    temp += year_list[-2][1]
                    temp += year_list[-1][1]
                    year_trigger2 = False
                else:
                    temp += year_list[-2][1]*10
                    temp += year_list[-1][1]
                    year_trigger2 = False


            if len(year_list) == 2 and year_trigger1 and year_trigger2:
                # temp2 = 0
                if year_list[0][2] == 5:
                    temp = int('19'+str(year_list[0][1]+year_list[1][1]))
                else:
                    temp = int('19' + str(year_list[0][1]) + str(year_list[1][1]))
            # print(year_list[pos:])
            return {"day": day, "month": month, "year": temp}
            # for i in range(len(year_list)):
            #     if position == year_list[i][0]:
            #         continue
            #     if year_list[i][2] == 6 and year_list[i][1] == 2 and year_trigger:
            #         temp = 2
            #         year_trigger = False
            #     if year_list[i][2] == 7 and temp == 2 and not year_trigger:
            #         temp = 2000
            #         year_trigger = False
            #     if year_list[i][2] == 7 and temp == 0 and year_trigger:
            #         year = 1000
            #         year_trigger = False
            #         year_trigger= False
            #
            #         print(year, year_list)
            #     if len(year_list) == 2 and year_trigger:
            #         year = 1900 + year_list[0][1] * 10 + year_list[1][1]
            #         year_trigger = False



    # result = {
    #     "day": day,
    #     "month": month,
    #     "year": year
    # }
    #
    # # print(result)
    #
    # if day == 0 or month == 0:
    #     print("ERROR {}". format(result))
    # return result




with io.open('juniorDS_task.csv','r', encoding="utf-8") as file:
    text = []
    dates = []
    i = 0
    error = 0
    for row in file:
        if i == 0:
            i+=1
            continue
        date = row.split(',')[:-1]
        sentence = " ".join([x.strip() for x in row.split(',')[-1].split(' ') if x.strip() not in stopwords])
        dates.append(date)
        text.append(sentence)

        date_from_text = date_recognition(text=sentence)

        # print("{} {} {}".format(date, sentence, date_from_text))
        if int(date[0]) != date_from_text['day'] or int(date[1]) != date_from_text['month'] or int(date[2]) != date_from_text['year']:
            error += 1
            print("{} {}".format(date, date_from_text))
    print(error)





