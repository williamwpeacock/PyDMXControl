from PyDMXControl.controllers import OpenDMXController as Controller

from PyDMXControl import Colors
from PyDMXControl.animations import Animation, GenericAnimation, CompoundAnimation, RandomAnimation

class Pulse(GenericAnimation):

    def __init__(self, max_value, attack = 0.1, delay = 0.25):
        min_value = 0
        if isinstance(max_value, list):
            min_value = [0] * len(max_value)

        super().__init__([(0, min_value), (attack, max_value), (delay, min_value)])

class Set(GenericAnimation):

    def __init__(self, value, length):
        min_value = 0
        if isinstance(value, list):
            min_value = [0] * len(value)
        super().__init__([(0, value), (length, value), (length, min_value)])

#### UTILS #####

white_flash = Pulse(Colors.White, 0.05, 0.1)

##### SETUP #####

dmx = Controller()
dmx.json.load_config('dj_lights.json')

lights = []
for light in dmx.get_all_fixtures():
    light.dim(255, 0)
    light.color(Colors.Black, 0)
    lights.append(light)

##### ANIMATION DEFINITIONS (8 bars) #####

# Chill

chill_8_0 = CompoundAnimation([
    (GenericAnimation([(0, Colors.Magenta), (4, Colors.Red), (8, Colors.Magenta)]), lights[0].color, 0, False, 1),
    (GenericAnimation([(0, Colors.Magenta), (4, Colors.Blue), (8, Colors.Magenta)]), lights[1].color, 0, False, 1),
    (GenericAnimation([(0, Colors.Red), (4, Colors.Magenta), (8, Colors.Red)]), lights[2].color, 0, False, 1),
    (GenericAnimation([(0, Colors.Blue), (4, Colors.Magenta), (8, Colors.Blue)]), lights[3].color, 0, False, 1),
], length = 8)

chill_8_1 = CompoundAnimation([
    (GenericAnimation([(0, Colors.Magenta), (2, Colors.Blue), (6, Colors.Red), (8, Colors.Magenta)]), lights[0].color, 0, False, 1),
    (GenericAnimation([(0, Colors.Magenta), (4, Colors.Red), (8, Colors.Magenta)]), lights[1].color, 0, False, 1),
    (GenericAnimation([(0, Colors.Red), (4, Colors.Magenta), (8, Colors.Red)]), lights[2].color, 0, False, 1),
    (GenericAnimation([(0, Colors.Blue), (3, Colors.Magenta), (5, Colors.Magenta), (8, Colors.Blue)]), lights[3].color, 0, False, 1),
], length = 8)

chill_8_bank = RandomAnimation([
    chill_8_0,
    chill_8_1
], length = 8)

# Buildup

buildup_8_0 = CompoundAnimation([
    (CompoundAnimation([(white_flash, lights[0].color, 0, False, 1)], length = 1), None, 0, False, 4),
    (CompoundAnimation([(white_flash, lights[1].color, 0, False, 1)], length = 1), None, 0, False, 4),
    (CompoundAnimation([(white_flash, lights[2].color, 0, False, 1)], length = 1), None, 0, False, 4),
    (CompoundAnimation([(white_flash, lights[3].color, 0, False, 1)], length = 1), None, 0, False, 4),
    (CompoundAnimation([(white_flash, lights[0].color, 0, False, 1)], length = 0.5), None, 4, False, 4),
    (CompoundAnimation([(white_flash, lights[1].color, 0, False, 1)], length = 0.5), None, 4, False, 4),
    (CompoundAnimation([(white_flash, lights[2].color, 0, False, 1)], length = 0.5), None, 4, False, 4),
    (CompoundAnimation([(white_flash, lights[3].color, 0, False, 1)], length = 0.5), None, 4, False, 4),
    (CompoundAnimation([(white_flash, lights[0].color, 0, False, 1)], length = 0.25), None, 6, False, 4),
    (CompoundAnimation([(white_flash, lights[1].color, 0, False, 1)], length = 0.25), None, 6, False, 4),
    (CompoundAnimation([(white_flash, lights[2].color, 0, False, 1)], length = 0.25), None, 6, False, 4),
    (CompoundAnimation([(white_flash, lights[3].color, 0, False, 1)], length = 0.25), None, 6, False, 4),
    (CompoundAnimation([(white_flash, lights[0].color, 0, False, 1)], length = 0.125), None, 7, False, 4),
    (CompoundAnimation([(white_flash, lights[1].color, 0, False, 1)], length = 0.125), None, 7, False, 4),
    (CompoundAnimation([(white_flash, lights[2].color, 0, False, 1)], length = 0.125), None, 7, False, 4),
    (CompoundAnimation([(white_flash, lights[3].color, 0, False, 1)], length = 0.125), None, 7, False, 4)
], length = 8)

buildup_8_bank = RandomAnimation([
    buildup_8_0
], length = 8)

# Drop

drop_8_0 = CompoundAnimation([
    (GenericAnimation([(0, Colors.Green), (8, Colors.White)]), lights[0].color, 0, False, 1),
    (GenericAnimation([(0, Colors.White), (8, Colors.Green)]), lights[1].color, 0, False, 1),
    (GenericAnimation([(0, Colors.Green), (8, Colors.White)]), lights[2].color, 0, False, 1),
    (GenericAnimation([(0, Colors.White), (8, Colors.Green)]), lights[3].color, 0, False, 1)
], length = 8)

drop_8_bank = RandomAnimation([
    drop_8_0
], length = 8)

##### ANIMATION DEFINITIONS (16 bars) #####

# Chill

chill_16_0 = CompoundAnimation([
    (GenericAnimation([(0, Colors.Magenta), (8, Colors.Red), (16, Colors.Magenta)]), lights[0].color, 0, False, 1),
    (GenericAnimation([(0, Colors.Magenta), (8, Colors.Blue), (16, Colors.Magenta)]), lights[1].color, 0, False, 1),
    (GenericAnimation([(0, Colors.Red), (8, Colors.Magenta), (16, Colors.Red)]), lights[2].color, 0, False, 1),
    (GenericAnimation([(0, Colors.Blue), (8, Colors.Magenta), (16, Colors.Blue)]), lights[3].color, 0, False, 1)
], length = 16)

chill_16_1 = CompoundAnimation([
    (GenericAnimation([(0, Colors.Magenta), (4, Colors.Blue), (12, Colors.Red), (16, Colors.Magenta)]), lights[0].color, 0, False, 1),
    (GenericAnimation([(0, Colors.Magenta), (4, Colors.Red), (16, Colors.Magenta)]), lights[1].color, 0, False, 1),
    (GenericAnimation([(0, Colors.Red), (8, Colors.Magenta), (16, Colors.Red)]), lights[2].color, 0, False, 1),
    (GenericAnimation([(0, Colors.Blue), (6, Colors.Magenta), (10, Colors.Magenta), (16, Colors.Blue)]), lights[3].color, 0, False, 1)
], length = 16)

chill_16_bank = RandomAnimation([
    chill_16_0,
    chill_16_1
], length = 16)

# Buildup

buildup_16_0 = CompoundAnimation([
    (CompoundAnimation([(white_flash, lights[0].color, 0, False, 1)], length = 2), None, 0, False, 4),
    (CompoundAnimation([(white_flash, lights[1].color, 0, False, 1)], length = 2), None, 0, False, 4),
    (CompoundAnimation([(white_flash, lights[2].color, 0, False, 1)], length = 2), None, 0, False, 4),
    (CompoundAnimation([(white_flash, lights[3].color, 0, False, 1)], length = 2), None, 0, False, 4),
    (CompoundAnimation([(white_flash, lights[0].color, 0, False, 1)], length = 1), None, 8, False, 4),
    (CompoundAnimation([(white_flash, lights[1].color, 0, False, 1)], length = 1), None, 8, False, 4),
    (CompoundAnimation([(white_flash, lights[2].color, 0, False, 1)], length = 1), None, 8, False, 4),
    (CompoundAnimation([(white_flash, lights[3].color, 0, False, 1)], length = 1), None, 8, False, 4),
    (CompoundAnimation([(white_flash, lights[0].color, 0, False, 1)], length = 0.5), None, 12, False, 4),
    (CompoundAnimation([(white_flash, lights[1].color, 0, False, 1)], length = 0.5), None, 12, False, 4),
    (CompoundAnimation([(white_flash, lights[2].color, 0, False, 1)], length = 0.5), None, 12, False, 4),
    (CompoundAnimation([(white_flash, lights[3].color, 0, False, 1)], length = 0.5), None, 12, False, 4),
    (CompoundAnimation([(white_flash, lights[0].color, 0, False, 1)], length = 0.25), None, 14, False, 4),
    (CompoundAnimation([(white_flash, lights[1].color, 0, False, 1)], length = 0.25), None, 14, False, 4),
    (CompoundAnimation([(white_flash, lights[2].color, 0, False, 1)], length = 0.25), None, 14, False, 4),
    (CompoundAnimation([(white_flash, lights[3].color, 0, False, 1)], length = 0.25), None, 14, False, 4),
    (CompoundAnimation([(white_flash, lights[0].color, 0, False, 1)], length = 0.125), None, 15, False, 4),
    (CompoundAnimation([(white_flash, lights[1].color, 0, False, 1)], length = 0.125), None, 15, False, 4),
    (CompoundAnimation([(white_flash, lights[2].color, 0, False, 1)], length = 0.125), None, 15, False, 4),
    (CompoundAnimation([(white_flash, lights[3].color, 0, False, 1)], length = 0.125), None, 15, False, 4)
], length = 16)

buildup_16_bank = RandomAnimation([
    buildup_16_0
], length = 16)

# Drop

kick = CompoundAnimation([
    (Pulse(Colors.White), lights[0].color, 0, False, 1),
], length = 1)

fast_kick = CompoundAnimation([
    (white_flash, lights[0].color, 0, False, 1),
], length = 1)

snare = CompoundAnimation([
    (white_flash, lights[1].color, 0, False, 1),
], length = 1)

kick_snare = CompoundAnimation([
    (kick, None, 0, False, 1), (snare, None, 0.25, False, 1), (kick, None, 0.5, False, 1), (snare, None, 0.75, False, 1)
], length = 1)

kick_snare_syncopated = CompoundAnimation([
    (kick, None, 0, False, 1), (snare, None, 0.25, False, 1), (fast_kick, None, 0.625, False, 1), (snare, None, 0.75, False, 1)
], length = 1)

kick_snare_snare = CompoundAnimation([
    (kick, None, 0, False, 1), (snare, None, 0.25, False, 1), (snare, None, 0.75, False, 1)
], length = 1)

kick_snare_snare_syncopated = CompoundAnimation([
    (kick, None, 0, False, 1), (snare, None, 0.25, False, 1), (snare, None, 0.625, False, 1)
], length = 1)

fancy_kick_stuff = CompoundAnimation([
    (kick, None, 0, False, 1), (snare, None, 0.25, False, 1), (kick, None, 0.375, False, 1), (fast_kick, None, 0.625, False, 1), (snare, None, 0.75, False, 1)
], length = 1)

drums_0 = CompoundAnimation([
    (CompoundAnimation([
        (kick_snare_syncopated, None, 0, False, 3),
        (fancy_kick_stuff, None, 3, False, 1)
    ]), None, 0, False, 4)
], length = 16)
drums_1 = CompoundAnimation([
    (kick_snare, None, 0, False, 16)
], length = 16)

drums = RandomAnimation([
    drums_0,
    drums_1
])

red_pulsing = CompoundAnimation([
    (Pulse(Colors.Red), lights[0].color, 0, False, 4),
    (Pulse(Colors.Red), lights[1].color, 0, False, 4),
    (Pulse(Colors.Red), lights[2].color, 0, False, 4),
    (Pulse(Colors.Red), lights[3].color, 0, False, 4)
], length = 1)

get_blue = CompoundAnimation([
    (GenericAnimation([(0, Colors.Black), (4, Colors.Blue)]), lights[0].color, 0, False, 1),
    (GenericAnimation([(0, Colors.Black), (4, Colors.Blue)]), lights[1].color, 0, False, 1),
    (GenericAnimation([(0, Colors.Black), (4, Colors.Blue)]), lights[2].color, 0, False, 1),
    (GenericAnimation([(0, Colors.Black), (4, Colors.Blue)]), lights[3].color, 0, False, 1),
])

def make_strobe(light, speed = 255, length = 0.5, color = Colors.Black):
    return CompoundAnimation([
        (Set(speed, length), light.strobe, 0, False, 1),
        (Set(color, length), light.color, 0, False, 1),
    ], length = length)

strobe_spin = CompoundAnimation([
    (make_strobe(lights[0], color = Colors.White), None, 0, False, 1),
    (make_strobe(lights[1], color = Colors.White), None, 0, False, 1)
], length = 4)

drop_16_0 = CompoundAnimation([
    (drums, None, 0, False, 1),
    (red_pulsing, None, 0, False, 16),
    (get_blue, None, 12, False, 1),
    (strobe_spin, None, 0, False, 4)
], length = 16)

drop_16_bank = RandomAnimation([
    drop_16_0
], length = 16)

##### START WEB CONTROLLER #####


anim_banks = {
    "chill_8": chill_8_bank,
    "buildup_8": buildup_8_bank,
    "drop_8": drop_8_bank,
    "chill_16": chill_16_bank,
    "buildup_16": buildup_16_bank,
    "drop_16": drop_16_bank
}

cbs = {
    "stop_animations", dmx.ticker.stop_animations
}

dmx.ticker.set_bpm(174)

dmx.web_control(port=8080, callbacks=cbs, animations=anim_banks)
dmx.sleep_till_enter()
dmx.close()