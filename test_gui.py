from PyDMXControl.controllers import OpenDMXController as Controller

from PyDMXControl import Colors
from PyDMXControl.animations import Pulse
from PyDMXControl.animations import Animation, GenericAnimation, CompoundAnimation, RandomAnimation

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
    flash = GenericAnimation([(0, Colors.Red), (0.05, Colors.White), (0.1, Colors.mix(Colors.Red, Colors.White, 0.15)), (0.15, Colors.Red)], [Animation.linear_color_mix, Animation.linear_color_mix, Animation.linear_color_mix])

    CompoundAnimation([(flash, lights[0].color, 0, False, 1),
                       (flash, lights[1].color, 0.25, False, 1),
    ], 0.5).start(dmx, None, 0, False, -1)

def spin():
    flash = GenericAnimation([(0, Colors.Black), (0.05, Colors.Red), (0.1, Colors.mix(Colors.Black, Colors.Red, 0.15)), (0.15, Colors.Black)], [Animation.linear_color_mix, Animation.linear_color_mix, Animation.linear_color_mix])

    anim_len = 0.25
    num_lights = 3
    CompoundAnimation([(flash, lights[i].color, i*(anim_len/num_lights), False, 1) for i in range(num_lights)], anim_len).start(dmx, None, 0, False, -1)

def buildup():
    flash = GenericAnimation([(0, Colors.Black), (0.05, Colors.White), (0.1, Colors.Black)], [Animation.linear_color_mix, Animation.linear_color_mix])

    anim_len = 16
    flashes_per_section = 8
    num_sections = 4
    light_anims = []
    for light in lights:
        light_anim_parts = []
        for i in range(num_sections):
            light_anim_parts.append((CompoundAnimation([ (flash, light.color, 0, 1) ], length = (anim_len/(2**(i+1)))/flashes_per_section), None, anim_len-(anim_len/(2**i)), flashes_per_section))

        light_anims.append((CompoundAnimation(light_anim_parts, length = anim_len), None, 0, 1))

    light_anims

    return CompoundAnimation(light_anims, length = anim_len)

def stop_animations():
    dmx.ticker.stop_animations()

def nudge_back():
    dmx.ticker.nudge(-50)

def nudge_forward():
    dmx.ticker.nudge(50)

def sync():
    dmx.ticker.sync()

cbs = {
    "generic_anim": generic_anim,
    "syncopated": syncopated,
    "normal": normal,
    "stop_animations": stop_animations,
    "nudge_back": nudge_back,
    "nudge_forward": nudge_forward,
    "sync": sync,
    "spin": spin,
    "buildup": buildup
}

chill_1 = CompoundAnimation([(GenericAnimation([(0, Colors.Red), (2, Colors.Blue), (4, Colors.Red)]), lights[0].color, 0, False, 4)], length = 16)
chill_2 = CompoundAnimation([(GenericAnimation([(0, Colors.Red), (2, Colors.Green), (4, Colors.Red)]), lights[0].color, 0, False, 4)], length = 16)

chill_bank = RandomAnimation([chill_1, chill_2], length = 16)

anim_banks = {
    "chill_16": chill_bank,
    "buildup_16": buildup()
}

dmx.ticker.set_bpm(176)

dmx.web_control(port=8080, callbacks=cbs, animations=anim_banks)
dmx.sleep_till_enter()
dmx.close()


# pulse = fixture.animate(targets=[CHANNEL_NUM], points=[(0, 0), (0.25, 255), (1, 0)], funcs=[linear, linear], repeat=1)
# strobe = fixture.animate(targets=[DIMMER_CHANNEL], speed=0.25, points=[(0, 255), (speed, 255), (speed, 0), (2*speed, 0)], repeat=4)

# speed_up_strobe = strobe.animate(targets=[speed], points=[(0, 0.1), (end, 0.01)])
