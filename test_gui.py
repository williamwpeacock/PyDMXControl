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
    pulse_0 = GenericAnimation([(0, Colors.Black), (0.1, Colors.Red), (0.25, Colors.Black)], [Animation.linear_color_mix, Animation.linear_color_mix])
    strobe_0 = GenericAnimation([(0, Colors.White), (0.05, Colors.White), (0.05, Colors.Black), (0.1, Colors.Black)], [Animation.linear_color_mix, Animation.linear_color_mix, Animation.linear_color_mix])
    
    CompoundAnimation([(pulse_0, lights[0].color, 0, False, 1), (pulse_0, lights[2].color, 0.25, False, 1),
                       (pulse_0, lights[1].color, 0.5, False, 1), (pulse_0, lights[3].color, 0.75, False, 1),
                       (pulse_0, lights[2].color, 1, False, 1), (pulse_0, lights[0].color, 1.25, False, 1),
                       (pulse_0, lights[3].color, 1.5, False, 1), (pulse_0, lights[1].color, 1.75, False, 1),
                       (pulse_0, lights[0].color, 2, False, 1), (pulse_0, lights[1].color, 2, False, 1),
                       (pulse_0, lights[2].color, 2, False, 1), (pulse_0, lights[3].color, 2, False, 1),
                       (strobe_0, lights[0].color, 2.5, False, 10), (strobe_0, lights[1].color, 2.5, False, 10),
                       (strobe_0, lights[2].color, 2.5, False, 10), (strobe_0, lights[3].color, 2.5, False, 10),
                       (pulse_0, lights[0].color, 3.5, False, 1), (pulse_0, lights[1].color, 3.5, False, 1),
                       (pulse_0, lights[2].color, 3.75, False, 1), (pulse_0, lights[3].color, 3.75, False, 1),
                       (pulse_0, lights[0].color, 4, False, 1), (pulse_0, lights[1].color, 4, False, 1),
                       (pulse_0, lights[2].color, 4, False, 1), (pulse_0, lights[3].color, 4, False, 1),
                       (strobe_0, lights[0].color, 4.5, False, 10), (strobe_0, lights[1].color, 4.5, False, 10),
                       (strobe_0, lights[2].color, 4.5, False, 10), (strobe_0, lights[3].color, 4.5, False, 10),
                       (pulse_0, lights[0].color, 5.5, False, 1), (pulse_0, lights[2].color, 5.5, False, 1),
                       (pulse_0, lights[1].color, 5.75, False, 1), (pulse_0, lights[3].color, 5.75, False, 1),
                       (pulse_0, lights[0].color, 6, False, 1), (pulse_0, lights[1].color, 6, False, 1),
                       (pulse_0, lights[2].color, 6, False, 1), (pulse_0, lights[3].color, 6, False, 1),
                       (pulse_0, lights[0].color, 6.25, False, 1), (pulse_0, lights[1].color, 6.333, False, 1),
                       (pulse_0, lights[2].color, 6.417, False, 1),
                       (pulse_0, lights[0].color, 6.5, False, 1), (pulse_0, lights[1].color, 6.5, False, 1),
                       (pulse_0, lights[2].color, 6.75, False, 1), (pulse_0, lights[3].color, 6.75, False, 1),
                       (pulse_0, lights[0].color, 7, False, 1), (pulse_0, lights[1].color, 7, False, 1),
                       (pulse_0, lights[2].color, 7.25, False, 1), (pulse_0, lights[3].color, 7.25, False, 1),
    ]).start(dmx, None, 0, False, 1)

def syncopated():
    flash = GenericAnimation([(0, Colors.Black), (0.05, Colors.White), (0.1, Colors.mix(Colors.Black, Colors.White, 0.15)), (0.15, Colors.Black)], [Animation.linear_color_mix, Animation.linear_color_mix, Animation.linear_color_mix])

    CompoundAnimation([(flash, lights[0].color, 0, False, 1),
                       (CompoundAnimation([(flash, lights[3].color, 0, False, 1)], 0.5), None, 0.25, False, 2),
                       (flash, lights[0].color, 0.625, False, 1),
    ], 1).start(dmx, None, 0, False, -1)

def normal():
    flash = GenericAnimation([(0, Colors.Black), (0.05, Colors.White), (0.1, Colors.mix(Colors.Black, Colors.White, 0.15)), (0.15, Colors.Black)], [Animation.linear_color_mix, Animation.linear_color_mix, Animation.linear_color_mix])

    CompoundAnimation([(flash, lights[0].color, 0, False, 1),
                       (flash, lights[1].color, 0.25, False, 1),
    ], 0.5).start(dmx, None, 0, True, -1)


def stop_animations():
    dmx.ticker.stop_animations()

def nudge_back():
    dmx.ticker.nudge(-50)
    
def nudge_forward():
    dmx.ticker.nudge(50)

def sync():
    dmx.ticker.sync()

anims = {
    "generic_anim": generic_anim,
    "syncopated": syncopated,
    "normal": normal,
    "stop_animations": stop_animations,
    "nudge_back": nudge_back,
    "nudge_forward": nudge_forward,
    "sync": sync, 
}

dmx.ticker.set_bpm(160)

dmx.web_control(port=8080, callbacks=anims)
dmx.sleep_till_enter()
dmx.close()


# pulse = fixture.animate(targets=[CHANNEL_NUM], points=[(0, 0), (0.25, 255), (1, 0)], funcs=[linear, linear], repeat=1)
# strobe = fixture.animate(targets=[DIMMER_CHANNEL], speed=0.25, points=[(0, 255), (speed, 255), (speed, 0), (2*speed, 0)], repeat=4)

# speed_up_strobe = strobe.animate(targets=[speed], points=[(0, 0.1), (end, 0.01)])