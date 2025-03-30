from CompIntel_DB import CompIntel_DB
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
        X.bar_chart_grouped("Graduation Rates.csv", colors=["purple", "gold"], percent=True)
    if i == 5:
        X = DV("DataPacket")
        for pie_data in ["Gender.csv", "Home State.csv", "Load.csv", "Race.csv", "Status.csv"]:
            X.pie_chart(pie_data)


if __name__ == '__main__':
    f(4)
