from matplotlib import pyplot
from numpy.lib.function_base import median
import json
import numpy as np
import statistics
import Utilities

def generic_normalized_plot(data_array):
    for dt in data_array:
        normalized = [x - dt[0] for x in dt]
        pyplot.plot(normalized)

    pyplot.show()

def raw_plot(data):
    for d in data:
        print(d["marker"])
        pyplot.plot(d["smoothed"], '-D', markevery=[d["marker"]],
                    label=d["condition"] + ' ' + d["label_suffix"])
    pyplot.legend()
    pyplot.show()


def single_plot_with_label(data_array, xLabel, yLabel, title, save=False):
    fig, ax = pyplot.subplots()
    ax.plot(data_array)
    ax.set(xlabel=xLabel, ylabel=yLabel, title=title)
    pyplot.show()


def predecision_raw_plot(data):
    for d in data:
        pyplot.plot(d["decision_phase"], '-',
                    label=d["condition"] + ' ' + d["label_suffix"])
    pyplot.legend()
    pyplot.show()


def predecision_gradient_plot(data):
    for d in data:
        f = np.array(d["decision_phase"], dtype=float)
        data_gradient = np.gradient(f)
        pyplot.plot(data_gradient)
    pyplot.show()

def get_bs_mean_difference(data, scope):
    for d in data:
        pyplot.scatter(statistics.mean(d[scope]), 
            y =-0.1 if d["condition"]=='Free' else 0.1,
            marker='^' if d["condition"]=='Free' else 'o',
            c='#000000')
    pyplot.legend()
    pyplot.show()

def predecission_delta_plot(data, threshold):
    for d in data:
        f = np.array(d["decision_phase"], dtype=float)
        diff = np.diff(f)
        diff[abs(diff) < threshold] = 0

        # diff[diff<0]=-1
        # diff[diff>0]=1
        # diff = np.diff(diff)

        print(np.mean(diff))
        pyplot.plot(diff, label=d["condition"] + ' ' + d["label_suffix"])
    pyplot.legend()
    pyplot.show()


def predecission_scatter_plot_mean(data):
    for d in data:
        m = '^'
        y = -0.1
        if d["condition"] == "Free":
            m = 'o'
            y = 0.1
        print(statistics.mean(d["decision_phase"]))
        pyplot.scatter(statistics.mean(
            d["decision_phase"]), y, marker=m, c='#000000')
    pyplot.show()


def experiment():
    experiment_files = ["ExpData/M33_4.dat", "testFiles/sampleJson.dat", "testFiles/sampleJson2.dat", "ExpData/M27_3.dat", "ExpData/M31_2.dat"]
    scope = Utilities.Trial_Data.decision_phase
    row, col = Utilities.split_single_colunm(len(experiment_files))
    feedbackCondition = 1
    condition = Utilities.CONDITIONS[2]
    i = 1
    for file in experiment_files:
        data = json.load(open(file))
        extracted = Utilities.extract_data(data, feedbackCondition = feedbackCondition)
        average_trend = Utilities.average_difference_within_condition(extracted, scope.name, condition)
        pyplot.subplot(row, col, i)
        pyplot.plot(average_trend["average_trend"])
        i += 1
    pyplot.suptitle("Average of all " + condition + " for different subjects. Feedback: " + str(feedbackCondition))
    pyplot.show()

def unit_data_comparison():
    file = "ExpData/M33_4.dat"
    feedbackCondition = 1
    index = 0
    data = json.load(open(file))
    extracted = Utilities.extract_data(data, feedbackCondition = feedbackCondition)
    pyplot.subplot(3, 1, 1)
    pyplot.plot(extracted[index][Utilities.Trial_Data.raw.name])    
    pyplot.title("RAW")
    pyplot.subplot(3, 1, 2)
    pyplot.plot(extracted[index][Utilities.Trial_Data.removed_ouliers.name])
    pyplot.title("Outliers removed")
    pyplot.subplot(3, 1, 3)
    pyplot.plot(extracted[index][Utilities.Trial_Data.smoothed.name])
    pyplot.title("Smoothed")
    pyplot.show()

    # data = json.load(open("ExpData/M33_4.dat"))
    # data = json.load(open("testFiles/sampleJson.dat"))
    # data = json.load(open("testFiles/sampleJson2.dat"))
    # extracted = Utilities.extract_data(data)
    # raw_plot(extracted)
    # predecision_raw_plot(extracted)
    # predecision_gradient_plot(extracted)
    # predecission_delta_plot(extracted, 0.005)
    # predecission_scatter_plot_mean(extracted)
    # Utilities.get_bs_mean_difference(extracted, "baseline_difference_decision_phase")
    # Utilities.average_difference_within_condition(extracted, "decision_phase", Utilities.CONDITIONS[2])

    # initial_decision_phase_data = [x["initial_decision_phase"] for x in extracted]
    # generic_normalized_plot(initial_decision_phase_data)
    # normalized_initial_decision_phase_data = get_normalized_data(initial_decision_phase_data)
    # mean_initial_decision_phase_data = get_mean_line(normalized_initial_decision_phase_data)
    # single_plot_with_label(mean_initial_decision_phase_data, "Time", "Dilation", "Mean Dilation")

    #decision_phase_data = [x["decision_phase"] for x in extracted]
    # generic_normalized_plot(decision_phase_data)


# experiment()
unit_data_comparison()
