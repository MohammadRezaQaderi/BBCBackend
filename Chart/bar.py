import matplotlib.pyplot as plt
import os
import matplotlib
import arabic_reshaper
from bidi.algorithm import get_display

font = {'family': 'B Zar'}
matplotlib.rc('font', **font)


def create_bar_chart(categories, title, values, colors, rotation, size, path, filename):
    path_to_save = os.path.join(path, filename)
    plt.figure(figsize=(10, size))
    reshaped_categories = [get_display(arabic_reshaper.reshape(category)) for category in categories]
    plt.bar(reshaped_categories, values, color=colors)
    plt.title(title, family='B Zar')
    plt.ylim(0, 100)
    plt.xticks(rotation=rotation, family='B Zar')
    plt.grid(False)
    if path_to_save:
        plt.savefig(path_to_save)
    plt.close()
    return path_to_save
