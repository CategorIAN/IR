from CompIntel_DV import CompIntel_DV
from CompIntel_DB import CompIntel_DB

def f(i):
    if i == 1:
        C = CompIntel_DB("Ian")
        C.savePriceChange(2018, 2022)
    if i == 2:
        C = CompIntel_DB("Ian")
        C.saveNetPrice(2017, 2021)
    if i == 3:
        B = CompIntel_DB("Ian")
        B.savePrice(2022)
    if i == 4:
        B = CompIntel_DB("Ian")
        B.saveIncomingFreshmanChange(2017)
    #=================================================================================
    if i == 5:
        V = CompIntel_DV("Ian")
        V.line_graph("UG Enrollment Percent Change Since 2017.csv", percent=True)
    if i == 6:
        V = CompIntel_DV("Ian")
        V.bar_chart_grouped("6-YR Graduation Rates - 2017 to 2021.csv")
    if i == 7:
        V = CompIntel_DV("Ian")
        V.bar_chart_grouped("Freshman to Sophomore Retention Rates - 2017 to 2021.csv")
    if i == 8:
        V = CompIntel_DV("Ian")
        V.bar_chart_grouped("Total Annual Price (Sticker Price) 2022-23.csv", money=True, colors=['purple', 'gold'])

if __name__ == '__main__':
    f(5)
