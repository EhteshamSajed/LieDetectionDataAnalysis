from matplotlib import pyplot
from numpy.lib.function_base import median
import OutlierDetector
import Smoother
import statistics
import math
import enum


class Trial_Data(enum.Enum):
    raw = 1
    removed_ouliers = 2
    marker = 3
    smoothed = 4
    condition = 5
    decision_phase = 6
    initial_decision_phase = 7
    baseline_difference = 8
    baseline_difference_decision_phase = 9
    label_suffix = 10


CONDITIONS = ['Free', 'True', 'Lie', 'All']
ANSWERES = ['Any', 'True', 'False']
DECISION_PHASE = 120  # 2 seconds
START_FRAME = 30
# POST_DECISION_PHASE = 60


def extract_data(data, search_from=0, count=30, feedbackCondition=0, participantAnswer=1, condition_index=3):
    pupilDataTrials = data['trials'][feedbackCondition]['pupilDataTrials']
    bs_mean = calculate_baseline_mean(data, feedbackCondition)
    extracted = []
    while (search_from < len(pupilDataTrials) and count > 0):
        pupil_data_trial = pupilDataTrials[search_from]
        if pupil_data_trial['participantAnswer'] != 0 and (condition_index == 3 or condition_index == pupil_data_trial['question']['condition']):
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
                    Trial_Data.raw.name: pupil_data_trial['pupilDiameter'],
                    Trial_Data.removed_ouliers.name: removed_ouliers,
                    Trial_Data.marker.name: marker,
                    Trial_Data.smoothed.name: smoothed,
                    Trial_Data.condition.name: CONDITIONS[pupil_data_trial['question']['condition']],
                    Trial_Data.label_suffix.name: str(pupil_data_trial['stimuliId']),
                    # from marker to preceeding n frames
                    Trial_Data.decision_phase.name: get_predecision_phase(smoothed, marker),
                    # from start to n frames
                    Trial_Data.initial_decision_phase.name: get_initial_decision_phase(smoothed),
                    Trial_Data.baseline_difference.name: [x - bs_mean for x in smoothed],
                    Trial_Data.baseline_difference_decision_phase.name: [
                        x - bs_mean for x in get_predecision_phase(smoothed, marker)]
                }
                extracted.append(trial)
                count -= 1
        search_from += 1
    return extracted


def assess_participants_answer(pupil_data_trial, expected_answer):
    if expected_answer == ANSWERES[0]:
        return True
    real_answer = 2
    if int(pupil_data_trial['question']['circleString']) > 10:
        real_answer = 1
    participant_answer = pupil_data_trial['participantAnswer']
    if pupil_data_trial['question']['condition'] == 2:
        if expected_answer == ANSWERES[1]:
            return real_answer != participant_answer
        else:
            return real_answer == participant_answer
    else:
        if expected_answer == ANSWERES[1]:
            return real_answer == participant_answer
        else:
            return real_answer != participant_answer


def calculate_baseline_mean(data, feedbackCondition=0):
    pupilDiameter = data['trials'][feedbackCondition]['pupilDataBaselines'][0]['pupilDiameter']
    return statistics.mean(pupilDiameter)


def get_predecision_phase(trial, marker):
    if marker > DECISION_PHASE:
        return trial[marker-DECISION_PHASE:marker]
    else:
        return trial[0:marker]


def get_initial_decision_phase(trial):
    return trial[START_FRAME: START_FRAME + DECISION_PHASE]


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


def average_within_condition(data, scope, condition=CONDITIONS[3]):
    average_trend = [0] * max([len(d[scope]) for d in data])
    # average_trend = [0] * len(data[0][scope])
    for d in data:
        if (d["condition"] == condition or condition == CONDITIONS[3]) and not math.isnan(d[scope][0]) and len(d[scope]) >= DECISION_PHASE:
            average_trend = [(g+h) for g, h in zip(d[scope], average_trend)]
    average_trend = [x / len(data) for x in average_trend]
    result = {
        "average_trend": average_trend,
        "legend": condition
    }
    return result


def split_single_colunm(n):
    col = math.ceil(math.sqrt(n))
    row = math.ceil(n/col)
    return row, col
