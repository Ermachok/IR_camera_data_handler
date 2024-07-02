import json
import bisect

def get_Xpoint(shot_num: int, times: list[float], timestamp_base: float) -> tuple[dict, dict]:
    with open(r'D:\mcc\sht_data\mcc_%d.json' % shot_num) as json_file:
        mcc_data = json.load(json_file)
        mcc_time = mcc_data['time']['variable']

    xpoint_cords = dict()
    separatrix_data = dict()
    for ms in times:
        index_time = bisect.bisect_right(mcc_time, ms / 1000)
        xpoint_cords[ms] = {'R': mcc_data['Rx']['variable'][index_time],
                           'Z': mcc_data['Zx']['variable'][index_time]}
        if ms == timestamp_base:
            body_r = [x / 100 for x in mcc_data['boundary']['rbdy']['variable'][index_time]]
            body_z = [x / 100 for x in mcc_data['boundary']['zbdy']['variable'][index_time]]

            leg1_r = [x / 100 for x in mcc_data['boundary']['rleg_1']['variable'][index_time]]
            leg1_z= [x / 100 for x in mcc_data['boundary']['zleg_1']['variable'][index_time]]

            leg2_r = [x / 100 for x in mcc_data['boundary']['rleg_2']['variable'][index_time]]
            leg2_z = [x / 100 for x in mcc_data['boundary']['zleg_2']['variable'][index_time]]

            separatrix_data = {'body':
                                   {'R': body_r,
                                    'Z': body_z},
                               'leg_1':
                                   {
                                    'R': leg1_r,
                                    'Z': leg1_z},
                               'leg_2':
                                   {
                                    'R': leg2_r,
                                    'Z': leg2_z},
                               'timepoint': timestamp_base}

    return xpoint_cords, separatrix_data


def get_ir_data(discharge_shots: list):
    all_shots = {}
    for shot_num in discharge_shots:
        file_path = 'data/Result_Temperature%d.csv' % shot_num

        with open(file_path, 'r') as data_file:
            data = data_file.readlines()
            result = {
                'times_ms': [],
                'radii': [],
            }

            for ind, line in enumerate(data):
                line_data_list = line.split(',')
                if ind == 0:
                    times = [float(time) for time in line_data_list[1:]]
                    result['times_ms'] = times
                    for time in times:
                        result[time] = []
                else:
                    result['radii'].append(float(line_data_list[0]))
                    for time_ind, temperature in enumerate(line_data_list[1:]):
                        result[times[time_ind]].append(float(temperature))

        all_shots[shot_num] = result

    return all_shots