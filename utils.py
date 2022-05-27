import json
from multiprocessing import Process
from typing import List, Dict, Union

from matplotlib import pyplot as plt

from motor import SimpleMotor


def run_parallel_motors(motors: List[SimpleMotor], plot=True) -> None:
    processes = []

    for motor in motors:
        processes.append(
            Process(target=motor.run, args=(plot, ))
        )

    for process in processes:
        process.start()

def save_history_dict(
        history: Dict,
        out_directory: str = "rpm_history.json"
) -> None:
    with open(out_directory, "w") as file:
        json.dump(history, file, indent=4)

def load_history_dict(
        history_path: str = "rpm_history.json"
) -> Dict:
    with open(history_path, "r") as file:
        return json.load(file)

def plot_histories(
        history: Union[Dict, str],
        xlabel: str,
        ylabel: str,
        title: str,
        figure_size: tuple = (8, 5),
        save: Union[str, bool] = False,
) -> None:
    """
    A function to plot history by loading it from file or just getting it
    on the run.
    :param xlabel: x-axis label.
    :param ylabel: y-axis label.
    :param title: plot title.
    :param figure_size: plot size.
    :param history: it can be the history file directory or a dict object
    representing a loaded history.
    :param save: by default it is false, and it won't save the plot as an image
    if it is a string, it will represent the image output directory
    :return: None
    """
    if isinstance(history, str):
        plot_history = load_history_dict("rpm_history.json")
    else:
        plot_history = history

    plt.figure(figsize=figure_size)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    for key in plot_history.keys():
        label = key.replace("_", " ").title()
        print(label)
        plt.plot(plot_history[key], label=label)
        plt.legend(loc="best")

    if save:
        plt.savefig(save)

    plt.show()
