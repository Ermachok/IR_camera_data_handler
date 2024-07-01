import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import bisect

discharge_shots = [44584, 44641, 44648, 44576]
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


fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
ax.set_xlabel('R')
ax.set_ylabel('Temperature')


lines = {}
for shot_num in discharge_shots:
    line, = ax.plot(all_shots[shot_num]['radii'], [0 for _ in range(len(all_shots[shot_num]['radii']))],
                    label=shot_num)
    lines[shot_num] = line


def update(val):
    all_values = []
    for shot_num in discharge_shots:
        try:
            time = slider.val
            ir_camera_time_ind = bisect.bisect_left(all_shots[shot_num]['times_ms'], time)
            ir_camera_time = all_shots[shot_num]['times_ms'][ir_camera_time_ind]

            lines[shot_num].set_ydata(all_shots[shot_num][ir_camera_time])

            all_values.extend(all_shots[shot_num][ir_camera_time])
        except Exception as e:
            print(e)
            print('Discharge has already ended')
            lines[shot_num].set_ydata([0 for _ in range(len(all_shots[shot_num]['radii']))])

    ax.set_ylim(min(all_values) * 0.9, max(all_values) * 1.1)
    fig.canvas.draw_idle()


longest_discharge_duration = max([all_shots[shot_num]['times_ms'][-1] for shot_num in discharge_shots])
shortest_discharge_duration = min([all_shots[shot_num]['times_ms'][0] for shot_num in discharge_shots])

ax_slider = fig.add_axes([0.25, 0.1, 0.65, 0.03])
slider = Slider(ax_slider, 'Time, ms', shortest_discharge_duration, longest_discharge_duration,
                valinit=min(result['times_ms']),
                valstep=result['times_ms'][1] - result['times_ms'][0])

slider.on_changed(update)
ax.legend()
plt.show()
