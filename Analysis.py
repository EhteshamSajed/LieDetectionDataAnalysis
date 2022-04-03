from cProfile import label
from locale import normalize
from tkinter import font
from matplotlib import pyplot
from numpy.lib.function_base import median
import json
import numpy as np
import statistics

from sympy import false, true
import Utilities
import OutlierDetector
from os import listdir
import Smoother

pyplot.rcParams.update({'font.size': 12})

colorDictionary = {
    0: "k",
    1: "b",
    2: "r",
    3: "g",
    4: "c",
    5: "y"
}

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


# def predecision_gradient_plot(data):
#     for d in data:
#         f = np.array(d["decision_phase"], dtype=float)
#         data_gradient = np.gradient(f)
#         pyplot.plot(data_gradient)
#     pyplot.show()


def scatter_plot_mean():
    file = "ExpData/V2/M25_5.dat"
    # file = "ExpData/V2/M31_6.dat"
    scope = Utilities.Trial_Data.decision_phase
    # scope = Utilities.Trial_Data.baseline_difference_decision_phase
    feedbackCondition = 1
    data = json.load(open(file))
    extracted = Utilities.extract_data(
        data, feedbackCondition=feedbackCondition, participantAnswer=0)
    for d in extracted:
        pyplot.scatter(statistics.mean(d[scope.name]),
                       y=-0.1 if d["condition"] == 'Free' else 0.1,
                       marker='^' if d["condition"] == 'Free' else 'o',
                       c='#000000')
    pyplot.legend()
    pyplot.show()


def delta_plot():
    file = "ExpData/V2/M25_5.dat"
    # file = "ExpData/V2/M31_6.dat"
    scope = Utilities.Trial_Data.decision_phase
    # scope = Utilities.Trial_Data.baseline_difference_decision_phase
    search_from = 0
    count = 3
    feedbackCondition = 0
    condition = 1
    threshold = 0.005
    data = json.load(open(file))
    extracted = Utilities.extract_data(
        data, search_from=search_from, count=count, feedbackCondition=feedbackCondition, participantAnswer=0, condition_index=condition)
    for d in extracted:
        f = np.array(d[scope.name], dtype=float)
        diff = np.diff(f)
        diff[abs(diff) < threshold] = 0

        # diff[diff<0]=-1
        # diff[diff>0]=1
        # diff = np.diff(diff)

        print(np.mean(diff))
        pyplot.plot(diff, label=d["condition"] + ' ' + d["label_suffix"])
        count -= 1
        search_from += 1
    pyplot.legend()
    pyplot.show()


# def predecission_scatter_plot_mean(data):
#     for d in data:
#         m = '^'
#         y = -0.1
#         if d["condition"] == "Free":
#             m = 'o'
#             y = 0.1
#         print(statistics.mean(d["decision_phase"]))
#         pyplot.scatter(statistics.mean(
#             d["decision_phase"]), y, marker=m, c='#000000')
#     pyplot.show()


def single_subject_average_within_condition():
    # experiment_files = ["ExpData/M33_4.dat", "testFiles/sampleJson.dat",
    # "testFiles/sampleJson2.dat", "ExpData/M27_3.dat", "ExpData/M31_2.dat"]
    # experiment_files = ["ExpData/V2/M25_5.dat"]
    # experiment_files = ["ExpData/V2/F27_19.dat"]
    # experiment_files = ["ExpData/V2/F24_13.dat"]
    experiment_files = ["ExpData/V2/M25_5.dat", "ExpData/V2/M31_6.dat",
                        "ExpData/V2/M28_7.dat", "ExpData/V2/F22_8.dat"]
    scope = Utilities.Trial_Data.baseline_difference
    # scope = Utilities.Trial_Data.baseline_difference_decision_phase
    # scope = Utilities.Trial_Data.decision_phase
    row, col = Utilities.split_single_colunm(len(experiment_files))
    feedbackCondition = 0
    condition_index = 0
    search_from = 0
    count = 30
    condition = Utilities.CONDITIONS[condition_index]
    i = 1
    for file in experiment_files:
        data = json.load(open(file))
        extracted = Utilities.extract_data(
            data=data, search_from=search_from, count=count, feedbackCondition=feedbackCondition, 
            participantAnswer=0, condition_index=condition_index, baseline_source=Utilities.Baseline_Source.preceding_trial)
        if len(extracted) == 0:
            continue
        average_trend = Utilities.average_within_condition(
            extracted, scope.name, condition)
        # print (average_trend["average_trend"])
        pyplot.subplot(row, col, i)
        # pyplot.plot(average_trend["average_trend"], label=data["participantName"])
        pyplot.plot(average_trend["average_trend"], '-D', label=data["participantName"], 
                    markevery = [int (average_trend["average_elapsed_ticks_to_answer"]/10000000 * 60)])
        pyplot.legend()
        i += 1
    pyplot.suptitle("Average of all " + condition +
                    " for different subjects. Feedback: " + str(feedbackCondition))
    pyplot.show()

def combined_average_all_decision():
    dir = "ExpData/V2/"
    experiment_files = listdir(dir)
    # experiment_files = ["M25_5.dat", "M31_6.dat", "F22_8.dat"]
    # experiment_files = ["M28_7.dat"]
    # experiment_files = ["F21_9.dat", "F21_16.dat", "F22_8.dat",
    #                     "F23_15.dat", "F23_20.dat", "F24_13.dat"]
    # experiment_files = ["F27_19.dat", "F29_14.dat", "M24_18.dat",
    #                     "M25_5.dat", "M26_10.dat", "M26_12.dat"]
    # experiment_files = ["M26_17.dat", "M28_7.dat", "M31_6.dat",
    #                     "M31_11.dat"]
    # experiment_files = ["F21_9.dat"]    
    feedbackCondition = 1
    search_from = 0
    count = 30
    conditions = [2, 1, 4, 5]    
    trial_counts = []
    normalize = False
    for condition_index in conditions:        
        trial_count = 0
        condition = Utilities.CONDITIONS[condition_index]
        average_trend = []
        for file in experiment_files:
            data = json.load(open(dir + file))
            extracted = Utilities.extract_data(
                data=data, search_from=search_from, count=count, feedbackCondition=feedbackCondition, participantAnswer=0,
                    condition_index=condition_index, baseline_source=Utilities.Baseline_Source.preceding_trial, skip_early_decision_phase=True
            )
            if len(extracted) == 0:
                continue
            trial_count += len(extracted)
            average_within_condition_decision_phase = Utilities.average_within_condition(
                    extracted, Utilities.Trial_Data.baseline_difference_decision_phase.name, condition)

            if len(average_trend) == 0:
                average_trend = average_within_condition_decision_phase["average_trend"]
            else:
                average_trend = [(x + y)/2 for x, y in zip(average_trend,
                                    average_within_condition_decision_phase["average_trend"])]
        smoothed = Smoother.smooth(average_trend, 10, True)
        if normalize:
            smoothed = [x - smoothed[0] for x in smoothed]
        pyplot.plot(smoothed , '-', label=condition, color=colorDictionary[condition_index])
        trial_counts.append(trial_count)
    print("*** Total number of trials ***")
    print(trial_counts)
    pyplot.legend()
    pyplot.suptitle("Combined Average of all subjects. Feedback: " + str(feedbackCondition))
    pyplot.show()
            
def combined_average_all():
    dir = "ExpData/V2/"
    experiment_files = listdir(dir)
    scope = Utilities.Trial_Data.baseline_difference
    # scope = Utilities.Trial_Data.baseline_difference_decision_phase
    # scope = Utilities.Trial_Data.removed_ouliers
    # scope = Utilities.Trial_Data.initial_decision_phase
    feedbackCondition = 0
    search_from = 0
    count = 30
    conditions = [2, 1, 4, 5]
    normalize = true
    # conditions = [0, 2, 1]
    # conditions = [5]
    for condition_index in conditions:
        i = 0
        condition = Utilities.CONDITIONS[condition_index]
        average_trend = []
        average_response_time = 0;
        for file in experiment_files:
            data = json.load(open(dir + file))
            extracted = Utilities.extract_data(
                data=data, search_from=search_from, count=count, feedbackCondition=feedbackCondition, participantAnswer=0,
                    condition_index=condition_index, baseline_source=Utilities.Baseline_Source.preceding_trial
            )
            if len(extracted) == 0:
                continue
            average_within_condition = Utilities.average_within_condition(
                    extracted, scope.name, condition)
            average_response_time += average_within_condition["relative_average_elapsed_ticks_to_answer"]
            if len(average_trend) == 0:
                average_trend = average_within_condition["average_trend"]
            else:
                average_trend = [(x + y)/2 for x, y in zip(average_trend,
                                                        average_within_condition["average_trend"])]
            i += 1
        smoothed = Smoother.smooth(average_trend, 10, True)
        average_response_time = (average_response_time/i) / 10000000 * 60
        average_response_time = average_response_time if average_response_time <= len(smoothed) else len(smoothed)
        if normalize:
            smoothed = [x - smoothed[0] for x in smoothed]
        pyplot.plot(smoothed , '-o', markevery = [int (average_response_time)], label=condition, color=colorDictionary[condition_index])
        # pyplot.plot(Smoother.smooth(average_trend, 10, True) , '-o', markevery = [int (average_response_time)], label=condition, color=colorDictionary[condition_index])
    pyplot.legend()

    pyplot.suptitle("Combined Average of all subjects. Feedback: " + str(feedbackCondition))
    pyplot.show()

def individual_average_all():
    dir = "ExpData/V2/"
    experiment_files = listdir(dir)
    # experiment_files = ["M25_5.dat", "M31_6.dat", "F22_8.dat"]
    # experiment_files = ["M28_7.dat"]
    experiment_files = ["F21_9.dat", "F21_16.dat", "F22_8.dat",
                        "F23_15.dat", "F23_20.dat", "F24_13.dat"]
    # experiment_files = ["F27_19.dat", "F29_14.dat", "M24_18.dat",
    #                     "M25_5.dat", "M26_10.dat", "M26_12.dat"]
    # experiment_files = ["M26_17.dat", "M28_7.dat", "M31_6.dat",
    #                     "M31_11.dat"]
    row, col = Utilities.split_single_colunm(len(experiment_files))
    scope = Utilities.Trial_Data.baseline_difference
    # scope = Utilities.Trial_Data.baseline_difference_decision_phase
    feedbackCondition = 0
    search_from = 0
    count = 30
    conditions = [2, 1, 4, 5]
    normalize = False
    # conditions = [0, 2, 1]
    # conditions = [5]
    i = 1
    for file in experiment_files:
        data = json.load(open(dir + file))
        for condition_index in conditions:
            condition = Utilities.CONDITIONS[condition_index]
            extracted = Utilities.extract_data(
                data=data, search_from=search_from, count=count, feedbackCondition=feedbackCondition, 
                participantAnswer=0, condition_index=condition_index, baseline_source=Utilities.Baseline_Source.preceding_trial)
            if len(extracted) == 0:
                continue
            average_trend = Utilities.average_within_condition(
                extracted, scope.name, condition)
            if normalize:
                average_trend = [x - average_trend[0] for x in average_trend]
            pyplot.subplot(row, col, i)
            # pyplot.plot(average_trend["average_trend"], label=data["participantName"])
            pyplot.plot(average_trend["average_trend"], '-D', label=condition, color=colorDictionary[condition_index], 
                        markevery = [int (average_trend["relative_average_elapsed_ticks_to_answer"]/10000000 * 60)])
            pyplot.legend()
        i += 1
    pyplot.suptitle("Combined Average of all subjects. Feedback: " + str(feedbackCondition))
    pyplot.show()

def single_subject_plot_within_condition():
    # file = "ExpData/V2/M25_5.dat"
    # file = "ExpData/V2/M31_6.dat"
    # file = "ExpData/V2/M28_7.dat"
    # file = "ExpData/V2/F22_8.dat"
    # file = "ExpData/V2/F21_9.dat"
    # file = "ExpData/V2/M26_10.dat"
    file = "ExpData/V2/M31_11.dat"
    # scope = Utilities.Trial_Data.decision_phase
    scope = Utilities.Trial_Data.baseline_difference_decision_phase
    # scope = Utilities.Trial_Data.smoothed
    # scope = Utilities.Trial_Data.removed_ouliers
    search_from = 0
    count = 30
    feedbackCondition = 0
    condition = 3
    i = 1
    data = json.load(open(file))
    extracted = Utilities.extract_data(
        data, search_from=search_from, count=count, feedbackCondition=feedbackCondition, participantAnswer=0, condition_index=condition,
        baseline_source=Utilities.Baseline_Source.preceding_trial)
    row, col = Utilities.split_single_colunm(len(extracted))
    # print (extracted[0][scope.name])
    for d in extracted:
        pyplot.subplot(row, col, i)
        pyplot.plot(d[scope.name], label=d[Utilities.Trial_Data.label_suffix.name] +
                    ":" + d[Utilities.Trial_Data.condition.name])
        pyplot.legend()
        i += 1
    pyplot.suptitle(data["participantName"] + ". Start index: " + str(search_from) + ", Ans Con " + Utilities.CONDITIONS[condition] +
                    ". Feedback: " + str(feedbackCondition))
    pyplot.show()


def single_subject_dynamic_difference():
    file = "ExpData/V2/M26_10.dat"
    # file = "ExpData/V2/M31_11.dat"
    scope = Utilities.Trial_Data.decision_phase
    search_from = 0
    count = 30
    feedbackCondition = 0
    condition = 3
    i = 1
    data = json.load(open(file))
    extracted = Utilities.extract_data(
        data, search_from=search_from, count=count, feedbackCondition=feedbackCondition, participantAnswer=0, condition_index=condition)
    row, col = Utilities.split_single_colunm(len(extracted))
    for d in extracted:
        pyplot.subplot(row, col, i)
        pyplot.plot(d[Utilities.Trial_Data.decision_phase.name] + d[Utilities.Trial_Data.post_decision_phase.name],
                '-D', markevery=[len(d[Utilities.Trial_Data.decision_phase.name])], label=d[Utilities.Trial_Data.label_suffix.name] +
                    ":" + d[Utilities.Trial_Data.condition.name])
        pyplot.legend()
        i += 1
    pyplot.suptitle(data["participantName"] + ". Start index: " + str(search_from) + ", Ans Con " + Utilities.CONDITIONS[condition] +
                    ". Feedback: " + str(feedbackCondition))
    pyplot.show()

def unit_data_comparison():
    file = "ExpData/M33_4.dat"
    file = "ExpData/V2/F27_19.dat"
    feedbackCondition = 1
    feedbackCondition = 0
    index = 0
    data = json.load(open(file))
    extracted = Utilities.extract_data(
        data, feedbackCondition=feedbackCondition, search_from=2, count=1)
    # extracted = Utilities.extract_data(
    #     data, feedbackCondition=feedbackCondition)
    pyplot.subplot(3, 1, 1)
    pyplot.plot(extracted[index][Utilities.Trial_Data.raw.name], label="RAW")
    pyplot.xlabel("number of frames")
    pyplot.ylabel("pupil size")
    pyplot.legend()
    # pyplot.title("RAW")
    pyplot.subplot(3, 1, 2)
    pyplot.plot(extracted[index][Utilities.Trial_Data.removed_ouliers.name], label="Outliers removed")
    pyplot.xlabel("number of frames")
    pyplot.ylabel("pupil size")
    pyplot.legend()
    # pyplot.title("Outliers removed")
    pyplot.subplot(3, 1, 3)
    pyplot.plot(extracted[index][Utilities.Trial_Data.smoothed.name], label="Smoothed")
    pyplot.xlabel("number of frames")
    pyplot.ylabel("pupil size")
    pyplot.legend()
    # pyplot.title("Smoothed")
    
    # pyplot.subplot(2, 1, 1)
    # pyplot.plot(extracted[index][Utilities.Trial_Data.removed_ouliers.name], label="Before Normalization")
    # pyplot.xlabel("number of frames")
    # pyplot.ylabel("pupil size")
    # pyplot.legend()
    # # pyplot.title("Before Normalization")
    # pyplot.subplot(2, 1, 2)
    # pyplot.plot(extracted[index][Utilities.Trial_Data.baseline_difference.name], label="After Normalization")
    # pyplot.xlabel("number of frames")
    # pyplot.ylabel("pupil size (Baseline difference)")
    # # pyplot.title("After Normalization")
    # pyplot.legend()
    
    pyplot.show()


def showZeroedOutliers():
    file = "ExpData/M33_4.dat"
    data = json.load(open(file))
    zeroed_outliers = OutlierDetector.remove_outliers(
        data['trials'][1]['pupilDataTrials'][0]['pupilDiameter'], False)
    pyplot.plot(zeroed_outliers)
    pyplot.show()


def plot_baseline():
    dir = "ExpData/V2/"
    experiment_files = listdir(dir)
    # experiment_files = ["F23_15.dat"]
    row, col = Utilities.split_single_colunm(len(experiment_files))
    feedbackCondition = 0
    i = 1
    for file in experiment_files:
        data = json.load(open(dir + file))
        pupilDiameter = data['trials'][feedbackCondition]['pupilDataBaselines'][0]['pupilDiameter'][Utilities.START_FRAME:]
        print (pupilDiameter)
        removed_ouliers = OutlierDetector.remove_outliers(
                    pupilDiameter, True)
        print (removed_ouliers)
        smoothed = Smoother.smooth(removed_ouliers, 10, True)
        print (smoothed)
        pyplot.subplot(row, col, i)
        pyplot.plot(smoothed,
                    label=data["participantName"])
        pyplot.legend()
        i += 1
    pyplot.suptitle("All smoothed Baseline. Feedback: " + str(feedbackCondition))
    pyplot.show()

# single_subject_average_within_condition()
# individual_average_all()
# combined_average_all()
combined_average_all_decision()
# unit_data_comparison()
# showZeroedOutliers()
# scatter_plot_mean()
# delta_plot()
# single_subject_plot_within_condition()
# single_subject_dynamic_difference()
# plot_baseline()