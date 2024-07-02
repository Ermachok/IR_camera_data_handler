import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import bisect

from utils import get_ir_data, get_Xpoint

discharge_shots = [44584, 44641, 44648, 44576]

all_shots = get_ir_data(discharge_shots)

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
                valinit=100,
                valstep=1)

slider.on_changed(update)
ax.legend()
plt.show()
