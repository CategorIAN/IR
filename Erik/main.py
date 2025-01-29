from CompIntel_DV import CompIntel_DV
from CompIntel_DB import CompIntel_DB

def f(i):
    if i == 1:
        C = CompIntel_DB("Ian")
        C.saveIncomingFreshmanChange(2017)
    if i == 2:
        C = CompIntel_DB("Ian")
        C.savePell(2017)
    if i == 3:
        B = CompIntel_DB("Ian")
        B.saveGender(2021)
    if i == 4:
        B = CompIntel_DB("Ian")
        B.saveIncomingFreshmanChange(2017)
    #=================================================================================
    if i == 5:
        V = CompIntel_DV("Ian")
        V.scatter("Percent of 2020-21 Student Body Receiving Pell and Change Since 2017.csv", percent=True)
    if i == 6:
        V = CompIntel_DV("Ian")
        V.bar_chart_stacked("Percent of White and Non-White - 2021.csv", colors=['purple', 'gold'], text_colors=['white', 'black'])
    if i == 7:
        V = CompIntel_DV("Ian")
        V.bar_chart_h("Degree Seeking Undergraduates - 2021.csv")
    if i == 8:
        V = CompIntel_DV("Ian")
        V.bar_chart_h("Change in Freshman Class Size 2017 to 2021.csv", percent=True)

if __name__ == '__main__':
    f(5)
