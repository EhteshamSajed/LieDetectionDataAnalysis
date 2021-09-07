from matplotlib import pyplot;
import OutlierDetector
import Smoother
import json;

# data = json.load(open("testFiles/sampleJson.dat"));
data = json.load(open("testFiles/sampleJson2.dat"));

# print (data['trials'][0]['pupilDataTrials'][0]['pupilDiameter'][0]);

# pyplot.plot(data['trials'][0]['pupilDataBaselines'][0]['pupilDiameter'], label = 'Baseline');

indexes = [2, 4, 10];
lbl = 'Free'
# indexes = [9, 6, 8];
# lbl = 'Lie'

for index in indexes:
    removed_ouliers = OutlierDetector.remove_outliers(data['trials'][0]['pupilDataTrials'][index]['pupilDiameter'])
    markerPos = []
    markerPos.append(OutlierDetector.relative_position_on_removed_outiler(removed_ouliers, int (data['trials'][0]['pupilDataTrials'][index]['elapseTicksToAnswer']/10000000 * 60)))
    smoothed = Smoother.smooth(removed_ouliers, 10, True)
    pyplot.plot(smoothed, '-D', markevery = markerPos, label = lbl +' ' + str (data['trials'][0]['pupilDataTrials'][index]['stimuliId']));
    # pyplot.plot(data['trials'][0]['pupilDataTrials'][index]['pupilDiameter'], '-D', markevery=markerPos, label = lbl +' ' + str (data['trials'][0]['pupilDataTrials'][index]['stimuliId']));

# for index in indexes:
#     markerPos = []
#     markerPos.append(int (data['trials'][0]['pupilDataTrials'][index]['elapseTicksToAnswer']/10000000 * 60))
#     pyplot.plot(data['trials'][0]['pupilDataTrials'][index]['pupilDiameter'], '-D', markevery=markerPos, label = lbl +' ' + str (data['trials'][0]['pupilDataTrials'][index]['stimuliId']));


# pyplot.plot(data['trials'][0]['pupilDataTrials'][2]['pupilDiameter'], label = 'Free ' + str (data['trials'][0]['pupilDataTrials'][2]['stimuliId']) + ' ans: ' + str (data['trials'][0]['pupilDataTrials'][2]['elapseTicksToAnswer']/10000000*60));
# pyplot.plot(data['trials'][0]['pupilDataTrials'][4]['pupilDiameter'], label = 'Free ' + str (data['trials'][0]['pupilDataTrials'][4]['stimuliId']) + ' ans: ' + str (data['trials'][0]['pupilDataTrials'][4]['elapseTicksToAnswer']/10000000*60));
# # pyplot.plot(data['trials'][0]['pupilDataTrials'][7]['pupilDiameter'], label = 'Free ' + str (data['trials'][0]['pupilDataTrials'][7]['stimuliId']) + ' ans: ' + str (data['trials'][0]['pupilDataTrials'][7]['elapseTicksToAnswer']/10000000*60));
# pyplot.plot(data['trials'][0]['pupilDataTrials'][10]['pupilDiameter'], label = 'Free ' + str (data['trials'][0]['pupilDataTrials'][10]['stimuliId']) + ' ans: ' + str (data['trials'][0]['pupilDataTrials'][10]['elapseTicksToAnswer']/10000000*60));
# markerPos = []
# markerPos.append(int (data['trials'][0]['pupilDataTrials'][9]['elapseTicksToAnswer']/10000000 * 60))
# pyplot.plot(data['trials'][0]['pupilDataTrials'][9]['pupilDiameter'], '-gD', markevery=markerPos, label = 'Lie ' + str (data['trials'][0]['pupilDataTrials'][9]['stimuliId']) + ' ans: ' + str (data['trials'][0]['pupilDataTrials'][9]['elapseTicksToAnswer']/10000000*60));
# pyplot.plot(data['trials'][0]['pupilDataTrials'][6]['pupilDiameter'], label = 'Lie ' + str (data['trials'][0]['pupilDataTrials'][6]['stimuliId']) + ' ans: ' + str (data['trials'][0]['pupilDataTrials'][6]['elapseTicksToAnswer']/10000000*60));
# #pyplot.plot(data['trials'][0]['pupilDataTrials'][8]['pupilDiameter'], label = 'Lie ' + str (data['trials'][0]['pupilDataTrials'][8]['stimuliId']) + ' ans: ' + str (data['trials'][0]['pupilDataTrials'][8]['elapseTicksToAnswer']/10000000*60));
# pyplot.plot(data['trials'][0]['pupilDataTrials'][12]['pupilDiameter'], label = 'Lie ' + str (data['trials'][0]['pupilDataTrials'][12]['stimuliId']) + ' ans: ' + str (data['trials'][0]['pupilDataTrials'][12]['elapseTicksToAnswer']/10000000*60));


# original = data['trials'][0]['pupilDataTrials'][4]['pupilDiameter']
# removed_ouliers = OutlierDetector.remove_outliers(original)
# markerpos = []
# markerpos.append(OutlierDetector.relative_position_on_removed_outiler(removed_ouliers, int (data['trials'][0]['pupilDataTrials'][4]['elapseTicksToAnswer']/10000000 * 60)))
# smoothed = Smoother.smooth(removed_ouliers, 10, True)
# # pyplot.plot(original, label = 'Free ' + str (data['trials'][0]['pupilDataTrials'][4]['stimuliId']) + ' ans: ' + str (data['trials'][0]['pupilDataTrials'][4]['elapseTicksToAnswer']/10000000*60));
# # pyplot.plot(removed_ouliers, label = 'removed outliers');
# pyplot.plot(smoothed, '-D', markevery = markerpos, label = 'smooth');


pyplot.legend();
pyplot.show();