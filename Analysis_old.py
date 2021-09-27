from matplotlib import pyplot
from numpy.lib.function_base import median
import OutlierDetector
import Smoother
import json
import numpy as np
import statistics
import math
import Utilities


CONDITIONS = ['Free', 'True', 'Lie']
ANSWERES = ['Any', 'True', 'False']
DECISION_PHASE = 120  # 2 seconds
START_FRAME = 30


def assess_participants_answer(pupil_data_trial, expected_answer):
    real_answer = 2
    if int(pupil_data_trial['question']['circleString']) > 10:
        real_answer = 1
    participant_answer = pupil_data_trial['participantAnswer']
    if pupil_data_trial['question']['condition'] == 0:
        if expected_answer == ANSWERES[0]:
            return True
        if expected_answer == ANSWERES[1]:
            return real_answer == participant_answer
        else:
            return real_answer != participant_answer

    if pupil_data_trial['question']['condition'] == 2:
        if expected_answer == ANSWERES[0]:
            return True
        if expected_answer == ANSWERES[1]:
            return real_answer != participant_answer
        else:
            return real_answer == participant_answer
    return False


# data = json.load(open("testFiles/sampleJson.dat"));
# data = json.load(open("testFiles/sampleJson2.dat"));
# data = json.load(open("ExpData/M33_4.dat"))

# pyplot.plot(data['trials'][0]['pupilDataBaselines'][0]['pupilDiameter'], label = 'Baseline raw');
# pyplot.plot(Smoother.smooth(OutlierDetector.remove_outliers(data['trials'][0]['pupilDataBaselines'][0]['pupilDiameter']), 10, True), label = 'Baseline processed');


def experiment_old(data):
    search_from = 15
    count = 100
    condition = 0
    condition = 2
    participantAnswer = 1

    pupilDataTrials = data['trials'][0]['pupilDataTrials']

    trials = []

    while (search_from < len(pupilDataTrials) and count > 0):
        pupil_data_trial = pupilDataTrials[search_from]
        if pupil_data_trial['participantAnswer'] != 0:
            if pupil_data_trial['question']['condition'] == condition and assess_participants_answer(pupil_data_trial, ANSWERES[participantAnswer]):
                removed_ouliers = OutlierDetector.remove_outliers(
                    pupil_data_trial['pupilDiameter'], True)
                markerPos = []
                markerPos.append(OutlierDetector.relative_position_on_removed_outiler(
                    removed_ouliers, int(pupil_data_trial['elapseTicksToAnswer']/10000000 * 60)))
                smoothed = Smoother.smooth(removed_ouliers, 10, True)
                trials.append(smoothed)
                lbl = CONDITIONS[condition]
                pyplot.plot(smoothed, '-D', markevery=markerPos,
                            label=lbl + ' ' + str(pupil_data_trial['stimuliId']))

                count -= 1
        search_from += 1
    pyplot.legend()
    pyplot.show()
    return trials


def extract_data(data):
    search_from = 0
    count = 3
    condition = 0
    # condition = 2
    participantAnswer = 1
    feedbackCondition = 0
    # feedbackCondition = 1

    pupilDataTrials = data['trials'][feedbackCondition]['pupilDataTrials']
    bs_mean = calculate_baseline_mean(data, feedbackCondition)

    extracted = []

    while (search_from < len(pupilDataTrials) and count > 0):
        pupil_data_trial = pupilDataTrials[search_from]
        if pupil_data_trial['participantAnswer'] != 0:
            if pupil_data_trial['question']['condition'] == condition and assess_participants_answer(pupil_data_trial, ANSWERES[participantAnswer]):
                removed_ouliers = OutlierDetector.remove_outliers(
                    pupil_data_trial['pupilDiameter'], True)
                markerPos = []
                markerPos.append(OutlierDetector.relative_position_on_removed_outiler(
                    removed_ouliers, int(pupil_data_trial['elapseTicksToAnswer']/10000000 * 60)))
                smoothed = Smoother.smooth(removed_ouliers, 10, True)
                marker = OutlierDetector.relative_position_on_removed_outiler(
                    removed_ouliers, int(pupil_data_trial['elapseTicksToAnswer']/10000000 * 60))                
                trial = {
                    "marker": marker,
                    "smoothed": smoothed,
                    "condition": CONDITIONS[condition],
                    "label_suffix": str(pupil_data_trial['stimuliId']),
                    # from marker to preceeding n frames
                    "decision_phase": get_predecision_phase(smoothed, marker),
                    # from start to n frames
                    "initial_decision_phase": get_initial_decision_phase(smoothed),
                    "baseline_difference": [x - bs_mean for x in smoothed],
                    "baseline_difference_decision_phase": [x - bs_mean for x in get_predecision_phase(smoothed, marker)]
                }
                extracted.append(trial)
                count -= 1
        search_from += 1
    return extracted


def average_difference_within_condition(data, scope, condition='Free'):
    average_trend = [0] * len(data[0][scope])
    for d in data:
        # print (d["condition"])
        # if d["condition"] == "Lie":
        if d["condition"] == condition and not math.isnan(d[scope][0]):
            average_trend = [(g+h) for g, h in zip (d[scope], average_trend)]
    average_trend = [x / len(data) for x in average_trend]    
    pyplot.plot(average_trend)
    pyplot.show()

def calculate_baseline_mean(data, feedbackCondition=0):
    pupilDiameter = data['trials'][feedbackCondition]['pupilDataBaselines'][0]['pupilDiameter']
    return statistics.mean(pupilDiameter)

def get_bs_mean_difference(data, scope):
    for d in data:
        pyplot.scatter(statistics.mean(d[scope]), 
            y =-0.1 if d["condition"]=='Free' else 0.1,
            marker='^' if d["condition"]=='Free' else 'o',
            c='#000000')
    pyplot.legend()
    pyplot.show()

def get_bs_difference (data, bs_mean, scope):
    for d in data:
        pyplot.scatter(statistics.mean([x - bs_mean for x in d[scope]]), 
            y =-0.1 if d["condition"]=='Free' else 0.1,
            marker='^' if d["condition"]=='Free' else 'o',
            c='#000000')
    pyplot.legend()
    pyplot.show()

# forgot to call assess_participants_answer()
def extract_data_for_scatter_plot(data):
    search_from = 0
    count = 30
    # condition = 0
    # condition = 2
    participantAnswer = 1
    feedbackCondition = 0
    # feedbackCondition = 1

    pupilDataTrials = data['trials'][feedbackCondition]['pupilDataTrials']
    bs_mean = calculate_baseline_mean(data, feedbackCondition)

    extracted = []

    while (search_from < len(pupilDataTrials) and count > 0):
        pupil_data_trial = pupilDataTrials[search_from]
        if pupil_data_trial['participantAnswer'] != 0:
            if assess_participants_answer(pupil_data_trial, ANSWERES[participantAnswer]):
                removed_ouliers = OutlierDetector.remove_outliers(
                    pupil_data_trial['pupilDiameter'], True)
                markerPos = []
                markerPos.append(OutlierDetector.relative_position_on_removed_outiler(
                    removed_ouliers, int(pupil_data_trial['elapseTicksToAnswer']/10000000 * 60)))
                smoothed = Smoother.smooth(removed_ouliers, 10, True)
                marker = OutlierDetector.relative_position_on_removed_outiler(
                    removed_ouliers, int(pupil_data_trial['elapseTicksToAnswer']/10000000 * 60))
                trial = {
                    "marker": marker,
                    "smoothed": smoothed,
                    "condition": CONDITIONS[pupil_data_trial['question']['condition']],
                    "label_suffix": str(pupil_data_trial['stimuliId']),
                    # from marker to preceeding n frames
                    "decision_phase": get_predecision_phase(smoothed, marker),
                    # from start to n frames
                    "initial_decision_phase": get_initial_decision_phase(smoothed),
                    "baseline_difference": [x - bs_mean for x in smoothed],
                    "baseline_difference_decision_phase": [x - bs_mean for x in get_predecision_phase(smoothed, marker)]
                }
                extracted.append(trial)
                count -= 1
        search_from += 1
    return extracted


def get_predecision_phase(trial, marker):
    if marker > DECISION_PHASE:
        return trial[marker-DECISION_PHASE:marker]
    else:
        return trial[0:marker]


def get_initial_decision_phase(trial):
    return trial[START_FRAME: START_FRAME + DECISION_PHASE]


def generic_normalized_plot(data_array):
    for dt in data_array:
        normalized = [x - dt[0] for x in dt]
        pyplot.plot(normalized)

    pyplot.show()


def get_normalized_data(data_array):
    normalized_array = []
    for dt in data_array:
        normalized = [x - dt[0] for x in dt]
        normalized_array.append(normalized)

    return normalized_array


def get_mean_line(data_array):
    mean_values = []
    max_len = max([len(x) for x in data_array])
    for i in range(max_len):
        valid_values = [x[i] for x in data_array if i < len(x)]
        mean_at_frame = sum(valid_values) / len(valid_values)
        mean_values.append(mean_at_frame)

    return mean_values


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
    # if save:
    #    fig.save()
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
    # data = json.load(open("ExpData/M33_4.dat"))
    # data = json.load(open("testFiles/sampleJson.dat"))
    data = json.load(open("testFiles/sampleJson2.dat"))
    # extracted = extract_data(data)
    # extracted = extract_data_for_scatter_plot(data)
    extracted = Utilities.extract_data(data)
    # raw_plot(extracted)
    # predecision_raw_plot(extracted)
    # predecision_gradient_plot(extracted)
    # predecission_delta_plot(extracted, 0.005)
    # predecission_scatter_plot_mean(extracted)
    # get_bs_mean_difference(extracted, calculate_baseline_mean(data), "decision_phase")
    # get_bs_mean_difference(extracted, "baseline_difference_decision_phase")
    average_difference_within_condition(extracted, "decision_phase", CONDITIONS[2])

    # initial_decision_phase_data = [x["initial_decision_phase"] for x in extracted]
    # generic_normalized_plot(initial_decision_phase_data)
    # normalized_initial_decision_phase_data = get_normalized_data(initial_decision_phase_data)
    # mean_initial_decision_phase_data = get_mean_line(normalized_initial_decision_phase_data)
    # single_plot_with_label(mean_initial_decision_phase_data, "Time", "Dilation", "Mean Dilation")

    #decision_phase_data = [x["decision_phase"] for x in extracted]
    # generic_normalized_plot(decision_phase_data)


experiment()
