from CompIntel_DB import CompIntel_DB
from CompIntel_DV import CompIntel_DV
from Carroll_DB import Carroll_DB
from IPEDS import IPEDS
from DV import DV

def f(i):
    if i == 1:
        pass
    if i == 2:
        pass
    if i == 3:
        X = DV("DataPacket")
        X.bar_chart_v("Enrollment.csv")
    if i == 4:
        X = DV("DataPacket")
        X.bar_chart_grouped("Graduation Rates (Draft 2).csv", colors=["purple", "gold"], percent=True)
    if i == 5:
        X = DV("DataPacket")
        for pie_data in ["Gender.csv", "Home State.csv", "Load.csv", "Race.csv", "Status.csv"]:
            X.pie_chart(pie_data)
        X.bar_chart_v("Enrollment.csv")
    if i == 6:
        X = CompIntel_DB("Ian")
        X.saveRetention(2019, 2023)
    if i == 7:
        X = CompIntel_DV("Ian")
        X.bar_chart_grouped("Freshman to Sophomore Retention Rates - 2019 to 2023.csv")
    if i == 8:
        X = CompIntel_DB("Ian")
        X.saveCarrollValues(2013, 2023)
    if i == 9:
        X = DV("DataPacket")
        X.pie_chart("Status (Draft 2).csv")
    if i == 10:
        X = DV("DataPacket")
        X.bar_chart_v("Enrollment (Draft 2).csv")


if __name__ == '__main__':
    f(5)
