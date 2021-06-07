import matplotlib.pyplot as plt
from datetime import datetime
import os

translate_dict = {
    'total_cases_highest_countries': '10 krajów z najwiekszą liczbą zakażeń na 1000 osób (łącznie)',
    'new_cases_highest_countries': '10 krajów z najwiekszą liczbą zakażeń na 1000 osób (nowych)',
    'total_deaths_highest_countries': '10 krajów z najwiekszą liczbą śmierci na 1000 osób (łącznie)',
    'new_deaths_highest_countries': '10 krajów z najwiekszą liczbą śmierci na 1000 osób (nowych)',
    'total_recovered_highest_countries': '10 krajów z najwiekszą liczbą ozdrowieńców na 1000 osób',
    'active_cases_highest_countries': '10 krajów z najwiekszą liczbą aktywnych przypadków na 1000 osób',
    'serious_cases_highest_countries': '10 krajów z najwiekszą liczbą poważnych przypadków na 1000 osób',
    'total_tests_highest_countries': '10 krajów z najwiekszą liczbą wykonanych testów na 1000 osób (łącznie)'
}

def draw_plots(data: dict):
    path = './plots/' + datetime.now().strftime("%m-%d-%Y/%H:%M:%S")
    os.makedirs(path)

    for key, value in data.items():
        value = dict(sorted(value.items(), key=lambda item: item[1]))
        total = value['Total']
        del value['Total']

        labels = [k + ' - ' + str(v) for k, v in value.items()]
        sizes = [ x / total for x in value.values()]

        fig, ax = plt.subplots()
        fig.set_size_inches(10,10)
        ax.pie(sizes, autopct='%1.1f%%', shadow=True, startangle=90)
        ax.axis('equal')

        plt.legend(labels, bbox_to_anchor=(1.15,0.5), loc="center")
        plt.title(translate_dict[key])
        plt.savefig( '%s/%s.png' % (path, key), bbox_inches="tight")
        plt.close()