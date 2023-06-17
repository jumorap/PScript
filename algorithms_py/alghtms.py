# los retornos "" o -1 hacen referencia a un error, probablemente escritura error

import matplotlib.pyplot as plt
import numpy as np
from colorama import init, Fore, Style

init()


def show_plot(values, plot_name):
    values = values.tolist()
    if type(values) != list:
        print(Fore.RED + "Error: The first parameter must be a list of floats." + Style.RESET_ALL)

    if type(plot_name) != str:
        print(Fore.RED + "Error: The second parameter must be a name without spaces." + Style.RESET_ALL)
    plt.plot(values)
    plt.title(plot_name)
    plt.draw()
    plt.savefig(f"results/plot/{plot_name}_plot.png")


def show_plot_histogram(values, plot_name):
    values = list(values)
    if type(values) != list:
        print(Fore.RED + "Error: The first parameter must be a list of floats." + Style.RESET_ALL)

    if type(plot_name) != str:
        print(Fore.RED + "Error: The second parameter must be a name without spaces." + Style.RESET_ALL)

    values.sort()
    num_bins = int(np.sqrt(len(values)))

    plt.hist(values, bins=num_bins)
    plt.title(plot_name)
    plt.draw()
    plt.savefig(f"results/plot/{plot_name}_histogram.png")
    plt.clf()
