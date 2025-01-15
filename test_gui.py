from PyDMXControl.controllers import GUIController as Controller

from PyDMXControl import Colors
from PyDMXControl.animations import Pulse
from PyDMXControl.animations import Animation, GenericAnimation, CompoundAnimation

dmx = Controller()
dmx.json.load_config('dj_lights.json')

lights = []
for light in dmx.get_all_fixtures():
    light.dim(255, 0)
    light.color(Colors.Black, 0)
    lights.append(light)

# def four_pulses():
#     Pulse(lights[0], Colors.Red, 0.1, 0.25).start(start_offset = 0, snap = False, repeat=8)
#     Pulse(lights[1], Colors.Green, 0.1, 0.25).start(start_offset = 0.5, snap = False, repeat=6)
#     Pulse(lights[2], Colors.Blue, 0.1, 0.25).start(start_offset = 1, snap = False, repeat=4)
#     Pulse(lights[3], Colors.White, 0.1, 0.25).start(start_offset = 1.5, snap = False, repeat=2)

def generic_anim():
    pulse_0 = GenericAnimation(lights[0].color, [(0, Colors.Black), (0.1, Colors.Red), (0.25, Colors.Black)], [Animation.linear_color_mix, Animation.linear_color_mix])
    pulse_1 = GenericAnimation(lights[1].color, [(0, Colors.Black), (0.1, Colors.Red), (0.25, Colors.Black)], [Animation.linear_color_mix, Animation.linear_color_mix])
    pulse_2 = GenericAnimation(lights[2].color, [(0, Colors.Black), (0.1, Colors.Red), (0.25, Colors.Black)], [Animation.linear_color_mix, Animation.linear_color_mix])
    pulse_3 = GenericAnimation(lights[3].color, [(0, Colors.Black), (0.1, Colors.Red), (0.25, Colors.Black)], [Animation.linear_color_mix, Animation.linear_color_mix])
    strobe_0 = GenericAnimation(lights[0].color, [(0, Colors.White), (0.05, Colors.White), (0.05, Colors.Black), (0.1, Colors.Black)], [Animation.linear_color_mix, Animation.linear_color_mix, Animation.linear_color_mix])
    strobe_1 = GenericAnimation(lights[1].color, [(0, Colors.White), (0.05, Colors.White), (0.05, Colors.Black), (0.1, Colors.Black)], [Animation.linear_color_mix, Animation.linear_color_mix, Animation.linear_color_mix])
    strobe_2 = GenericAnimation(lights[2].color, [(0, Colors.White), (0.05, Colors.White), (0.05, Colors.Black), (0.1, Colors.Black)], [Animation.linear_color_mix, Animation.linear_color_mix, Animation.linear_color_mix])
    strobe_3 = GenericAnimation(lights[3].color, [(0, Colors.White), (0.05, Colors.White), (0.05, Colors.Black), (0.1, Colors.Black)], [Animation.linear_color_mix, Animation.linear_color_mix, Animation.linear_color_mix])

    CompoundAnimation([(pulse_0, 0, False, 1), (pulse_2, 0.25, False, 1),
                       (pulse_1, 0.5, False, 1), (pulse_3, 0.75, False, 1),
                       (pulse_2, 1, False, 1), (pulse_0, 1.25, False, 1),
                       (pulse_3, 1.5, False, 1), (pulse_1, 1.75, False, 1),
                       (pulse_0, 2, False, 1), (pulse_1, 2, False, 1),
                       (pulse_2, 2, False, 1), (pulse_3, 2, False, 1),
                       (strobe_0, 2.5, False, 10), (strobe_1, 2.5, False, 10),
                       (strobe_2, 2.5, False, 10), (strobe_3, 2.5, False, 10),
                       (pulse_0, 3.5, False, 1), (pulse_1, 3.5, False, 1),
                       (pulse_2, 3.75, False, 1), (pulse_3, 3.75, False, 1),
                       (pulse_0, 4, False, 1), (pulse_1, 4, False, 1),
                       (pulse_2, 4, False, 1), (pulse_3, 4, False, 1),
                       (strobe_0, 4.5, False, 10), (strobe_1, 4.5, False, 10),
                       (strobe_2, 4.5, False, 10), (strobe_3, 4.5, False, 10),
                       (pulse_0, 5.5, False, 1), (pulse_2, 5.5, False, 1),
                       (pulse_1, 5.75, False, 1), (pulse_3, 5.75, False, 1),
                       (pulse_0, 6, False, 1), (pulse_1, 6, False, 1),
                       (pulse_2, 6, False, 1), (pulse_3, 6, False, 1),
                       (pulse_0, 6.25, False, 1), (pulse_1, 6.333, False, 1),
                       (pulse_2, 6.417, False, 1),
                       (pulse_0, 6.5, False, 1), (pulse_1, 6.5, False, 1),
                       (pulse_2, 6.75, False, 1), (pulse_3, 6.75, False, 1),
                       (pulse_0, 7, False, 1), (pulse_1, 7, False, 1),
                       (pulse_2, 7.25, False, 1), (pulse_3, 7.25, False, 1),
    ]).start(dmx, 0, False, 1)

anims = {
    "generic_anim": generic_anim
}

dmx.ticker.set_bpm(174)

dmx.web_control(port=8080, callbacks=anims)
dmx.sleep_till_enter()
dmx.close()


# pulse = fixture.animate(targets=[CHANNEL_NUM], points=[(0, 0), (0.25, 255), (1, 0)], funcs=[linear, linear], repeat=1)
# strobe = fixture.animate(targets=[DIMMER_CHANNEL], speed=0.25, points=[(0, 255), (speed, 255), (speed, 0), (2*speed, 0)], repeat=4)

# speed_up_strobe = strobe.animate(targets=[speed], points=[(0, 0.1), (end, 0.01)])