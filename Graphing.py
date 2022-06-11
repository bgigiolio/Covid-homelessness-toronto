import pandas as pd
from matplotlib import pyplot as plt


def plot_age():
    df = pd.DataFrame({'Age Group': ['0-19', '20-29', '30-39', '40-49', '50-59',
                                     '60-69', '70-79', '80-89', '90+'],
                       'Cases': [8093, 13317, 11092, 9487, 9882, 6326, 3312,
                                 3329, 2172]})
    graph = df.plot.bar(x="Age Group", y="Cases", title="Cases by Age Group",
                        xlabel="Age Group", ylabel="Cases")
    return graph


def plot_hospitalizations():
    df = pd.DataFrame({'Age Group': ['0-19', '20-29', '30-39', '40-49', '50-59',
                                     '60-69', '70-79', '80-89', '90+'],
                       'Hospitalizations': [56, 120, 192, 317, 576, 828, 881,
                                            1020, 517]})
    graph = df.plot.bar(x="Age Group", y="Hospitalizations",
                        title="Hospitalizations by Age Group",
                        xlabel="Age Group", ylabel="Hospitalizations")
    return graph


def plot_hospitalization_rate():
    df = pd.DataFrame({'Age Group': ['0-19', '20-29', '30-39', '40-49', '50-59',
                                     '60-69', '70-79', '80-89', '90+'],
                       'Hospitalization Rate': [56 / 8093, 120 / 13317,
                                                192 / 11092, 317 / 9487,
                                                576 / 9882, 828 / 6382,
                                                881 / 3312,
                                                1020 / 3329, 517 / 2172]})
    graph = df.plot.bar(x="Age Group", y="Hospitalization Rate",
                        title="Hospitalization Rate by Age Group",
                        xlabel="Age Group", ylabel="Hospitalization Rate")
    return graph


def occupancy_over_time():
    occ_df = pd.read_csv("occ_by_date.csv")
    cas_df = pd.read_csv("cases_over_time.csv")
    cas_df.set_axis(['Date', 'Cases'], axis=1, inplace=True)
    occ_df.set_axis(['Date', 'Occupancy'], axis=1, inplace=True)
    comb = pd.concat([occ_df, cas_df], axis=1)
    print(comb)

    ax1 = occ_df.plot.line(x="Date", y="Occupancy",
                           title="Toronto Shelter Occupancy and COVID Cases Over 2020",
                           figsize=(10, 6))
    ax2 = ax1.twinx()
    graph = cas_df.plot(ax=ax2, color="red")
    return graph


def occupancy_and_cases_by_FSA():
    total_df = pd.read_csv("shelter_cap_FSA.csv")
    total_df.set_axis(["FSA", "Occupancy", "Cases"], axis=1, inplace=True)


if __name__ == '__main__':
    fig1 = plot_age()
    plt.savefig('Case by age.png')
    fig2 = plot_hospitalizations()
    plt.savefig('Hospitalization by age.png')
    fig3 = plot_hospitalization_rate()
    plt.savefig('hospitalization rate by age.png')
    fig4 = occupancy_over_time()
    plt.savefig('Occupancy Over Time.png')
    plt.show()
