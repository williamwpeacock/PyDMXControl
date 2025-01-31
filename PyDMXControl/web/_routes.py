"""
 *  PyDMXControl: A Python 3 module to control DMX using OpenDMX or uDMX.
 *                Featuring fixture profiles, built-in effects and a web control panel.
 *  <https://github.com/MattIPv4/PyDMXControl/>
 *  Copyright (C) 2023 Matt Cowley (MattIPv4) (me@mattcowley.co.uk)
"""

from re import compile as re_compile  # Regex
from typing import List, Union, Tuple, Dict, Callable  # Typing
from collections import Counter

from flask import Blueprint, render_template, current_app, redirect, url_for, jsonify  # Flask

from .. import Colors  # Colors
from ..profiles.defaults import Fixture, Vdim  # Fixtures
from ..utils.exceptions import ChannelNotFoundException # Exceptions

routes = Blueprint('PyDMXControl', __name__, url_prefix='/')


def fixture_channels(this_fixture: Fixture) -> List[Tuple[str, int, int]]:
    chans = [(f['name'], fixture_channel_value(this_fixture, f['name']), fixture_channel_value(this_fixture, f['name'], True)) for f in this_fixture.channels.values()]
    if issubclass(type(this_fixture), Vdim):
        chans.append(("dimmer", fixture_channel_value(this_fixture, "dimmer"), fixture_channel_value(this_fixture, "dimmer", True)))
    return chans


def fixture_channel_value(this_fixture: Fixture, this_channel: Union[str, int], apply_parking: bool = False) -> int:
    if issubclass(type(this_fixture), Vdim):
        return this_fixture.get_channel_value(this_channel, False, apply_parking)[0]
    return this_fixture.get_channel_value(this_channel, apply_parking)[0]


helpers = ["on", "off", "locate"]


def fixture_helpers(this_fixture: Fixture) -> Dict[str, Callable]:
    return {f: this_fixture.__getattribute__(f) for f in helpers if hasattr(this_fixture, f)}


# Home
@routes.route('', methods=['GET'])
def home():
    fixture_types = Counter([type(x) for x in current_app.parent.controller.get_all_fixtures()])
    return render_template("index.jinja2", helpers=helpers, fixture_types=fixture_types)


# Global Intensity
@routes.route('intensity/<int:val>', methods=['GET'])
def global_intensity(val: int):
    if val < 0 or val > 255:
        return jsonify({"error": "Value {} is invalid".format(val)}), 400
    current_app.parent.controller.all_dim(val)
    return jsonify({"message": "All dimmers updated to {}".format(val)}), 200


# Fixture Home
@routes.route('fixture/<int:fid>', methods=['GET'])
def fixture(fid: int):
    this_fixture = current_app.parent.controller.get_fixture(fid)
    if not this_fixture:
        return redirect(url_for('.home'))
    return render_template("fixture.jinja2", fixture=this_fixture, fixture_channels=fixture_channels,
                           fixture_channel_value=fixture_channel_value, colors=Colors, helpers=helpers)


# Fixture Channel
@routes.route('fixture/<int:fid>/channel/<int:cid>', methods=['GET'])
def channel(fid: int, cid: int):
    this_fixture = current_app.parent.controller.get_fixture(fid)
    if not this_fixture:
        return redirect(url_for('.home'))

    try:
        chan = this_fixture.get_channel_id(cid)
    except ChannelNotFoundException:
        return redirect(url_for('.fixture', fid=this_fixture.id))

    this_channel = fixture_channels(this_fixture)[chan]
    return render_template("channel.jinja2", fixture=this_fixture, channel=this_channel, cid=chan)


# Fixture Channel Set
@routes.route('fixture/<int:fid>/channel/<int:cid>/<int:val>', methods=['GET'])
def channel_val(fid: int, cid: int, val: int):
    this_fixture = current_app.parent.controller.get_fixture(fid)
    if not this_fixture:
        return jsonify({"error": "Fixture {} not found".format(fid)}), 404

    try:
        chan = this_fixture.get_channel_id(cid)
    except ChannelNotFoundException:
        return jsonify({"error": "Channel {} not found".format(cid)}), 404

    if val < 0 or val > 255:
        return jsonify({"error": "Value {} is invalid".format(val)}), 400

    this_fixture.set_channel(chan, val)
    val = fixture_channel_value(this_fixture, chan)
    val_parked = fixture_channel_value(this_fixture, chan, True)
    data = {
        "message": "Channel {} {} updated to {}".format(
            this_fixture.start_channel + chan,
            this_fixture.channels[this_fixture.start_channel + chan]["name"],
            val
        ),
        "elements": {
            "channel-{}-value".format(chan): "{}{}".format(val, " ({})".format(val_parked) if this_fixture.parked else ""),
            "value": val,
            "slider_value": val
        }
    }
    if chan == this_fixture.get_channel_id("dimmer"):
        data["elements"]["intensity_value"] = val
    return jsonify(data), 200


# Fixture Color
@routes.route('fixture/<int:fid>/color/<string:val>', methods=['GET'])
def color(fid: int, val: str):
    this_fixture = current_app.parent.controller.get_fixture(fid)
    if not this_fixture:
        return jsonify({"error": "Fixture {} not found".format(fid)}), 404
    pattern = re_compile(r"^\s*(\d{1,3})\s*[, ]\s*(\d{1,3})\s*[, ]\s*(\d{1,3})\s*(?:[, ]\s*(\d{1,3})\s*)*$")
    match = pattern.match(val)
    if not match:
        return jsonify({"error": "Invalid color {} supplied".format(val)}), 400
    this_color = [int(f) for f in match.groups() if f]
    this_fixture.color(this_color)
    return jsonify({
        "message": "Color updated to {}".format(this_color),
        "elements": dict(
            {
                "value": Colors.to_hex(this_fixture.get_color())
            },
            **{"channel-{}-value".format(i): "{}{}".format(f[1], " ({})".format(f[2]) if this_fixture.parked else "")
               for i, f in enumerate(fixture_channels(this_fixture))}
        )
    }), 200


# Fixture Intensity
@routes.route('fixture/<int:fid>/intensity/<int:val>', methods=['GET'])
def intensity(fid: int, val: int):
    this_fixture = current_app.parent.controller.get_fixture(fid)
    if not this_fixture:
        return jsonify({"error": "Fixture {} not found".format(fid)}), 404

    try:
        chan = this_fixture.get_channel_id("dimmer")
    except ChannelNotFoundException:
        return jsonify({"error": "Dimmer channel not found"}), 404

    if val < 0 or val > 255:
        return jsonify({"error": "Value {} is invalid".format(val)}), 400

    this_fixture.set_channel(chan, val)
    val = fixture_channel_value(this_fixture, chan)
    val_parked = fixture_channel_value(this_fixture, chan, True)
    return jsonify({
        "message": "Dimmer updated to {}".format(val),
        "elements": {
            "channel-{}-value".format(chan): "{}{}".format(val, " ({})".format(val_parked) if this_fixture.parked else ""),
            "intensity_value": val
        }
    }), 200


# Fixture Helpers
@routes.route('fixture/<int:fid>/helper/<string:val>', methods=['GET'])
def helper(fid: int, val: str):
    this_fixture = current_app.parent.controller.get_fixture(fid)
    if not this_fixture:
        return jsonify({"error": "Fixture {} not found".format(fid)}), 404

    val = val.lower()
    this_helpers = fixture_helpers(this_fixture)
    if val not in this_helpers.keys():
        return jsonify({"error": "Helper {} not found".format(val)}), 404

    try:
        this_helpers[val]()
    except Exception:
        return jsonify({"error": "Helper {} failed to execute".format(val)}), 500
    return jsonify({
        "message": "Helper {} executed".format(val),
        "elements": dict(
            {
                "value": Colors.to_hex(this_fixture.get_color()),
                "intensity_value": fixture_channel_value(this_fixture, "dimmer")
            },
            **{"channel-{}-value".format(i): "{}{}".format(f[1], " ({})".format(f[2]) if this_fixture.parked else "")
               for i, f in enumerate(fixture_channels(this_fixture))}
        )
    }), 200


# Fixture Parking
@routes.route('fixture/<int:fid>/park', methods=['GET'])
def park(fid: int):
    this_fixture = current_app.parent.controller.get_fixture(fid)
    if not this_fixture:
        return jsonify({"error": "Fixture {} not found".format(fid)}), 404

    state = this_fixture.parked
    if state:
        this_fixture.unpark()
    else:
        this_fixture.park()
    state = not state

    return jsonify({
        "message": "Fixture {}".format("parked" if state else "unparked"),
        "elements": dict(
            {
                "parking": "Unpark" if state else "Park",
                "value": Colors.to_hex(this_fixture.get_color()),
                "intensity_value": fixture_channel_value(this_fixture, "dimmer")
            },
            **{"channel-{}-value".format(i): "{}{}".format(f[1], " ({})".format(f[2]) if this_fixture.parked else "")
               for i, f in enumerate(fixture_channels(this_fixture))}
        )
    }), 200


# Callbacks
@routes.route('callback/<string:cb>', methods=['GET'])
def callback(cb: str):
    if cb not in current_app.parent.callbacks.keys():
        return jsonify({"error": "Callback {} not found".format(cb)}), 404
    current_app.parent.callbacks[cb]()
    return jsonify({"message": "Callback {} executed".format(cb)}), 200
    # try:
    #     current_app.parent.callbacks[cb]()
    # except Exception:
    #     return jsonify({"error": "Callback {} failed to execute".format(cb)}), 500
    # return jsonify({"message": "Callback {} executed".format(cb)}), 200


# Timed Events
@routes.route('timed_event/<string:te>', methods=['GET'])
def timed_event(te: str):
    if te not in current_app.parent.timed_events.keys():
        return redirect(url_for('.home'))
    return render_template("timed_event.jinja2", te=te)


# Timed Events Data
@routes.route('timed_event/<string:te>/data', methods=['GET'])
def timed_event_data(te: str):
    if te not in current_app.parent.timed_events.keys():
        return jsonify({"error": "Timed Event {} not found".format(te)}), 404
    return jsonify({"data": current_app.parent.timed_events[te].data}), 200


# Timed Events Run
@routes.route('timed_event/<string:te>/run', methods=['GET'])
def run_timed_event(te: str):
    if te not in current_app.parent.timed_events.keys():
        return jsonify({"error": "Timed Event {} not found".format(te)}), 404
    try:
        current_app.parent.timed_events[te].run()
    except Exception:
        return jsonify({"error": "Timed Event {} failed to fire".format(te)}), 500
    return jsonify({"message": "Timed Event {} fired".format(te), "elements": {te + "-state": "Running"}}), 200


# Timed Events Stop
@routes.route('timed_event/<string:te>/stop', methods=['GET'])
def stop_timed_event(te: str):
    if te not in current_app.parent.timed_events.keys():
        return jsonify({"error": "Timed Event {} not found".format(te)}), 404
    try:
        current_app.parent.timed_events[te].stop()
    except Exception:
        return jsonify({"error": "Timed Event {} failed to stop".format(te)}), 500
    return jsonify({"message": "Timed Event {} stopped".format(te), "elements": {te + "-state": "Stopped"}}), 200

# @routes.route('', methods=['GET'])
# def custom_update_fixtures():
#     # show list of fixture types
#     # select fixture type:
#     #   show editable channel values
#     #   show list of fixtures of that type
#     #   show apply button
#     #   set channel values, select applicable fixtures, click apply
#     pass

# Fixture Type Home
@routes.route('fixture_type/<string:f_type>', methods=['GET'])
def fixture_type(f_type: str):
    fixtures = [f for f in current_app.parent.controller.get_all_fixtures()
                if type(f).__name__ == f_type]
    return render_template("fixture_type.jinja2", fixture_type=f_type, fixtures=fixtures,
                           fixture_channels=fixture_channels, colors=Colors)

@routes.route('bulk_change/<string:ids>/<string:values>', methods=['GET'])
def bulk_change(ids: str, values: str):
    for fid in ids.split('_'):
        try:
            fid = int(fid)
        except:
            return jsonify({"error": "{} is not an integer".format(fid)}), 404

        this_fixture = current_app.parent.controller.get_fixture(fid)
        if not this_fixture:
            return jsonify({"error": "Fixture {} not found".format(fid)}), 404

        channels_list = this_fixture.channels
        values_list = values.split('_')

        if not (len(channels_list) == len(values_list)):
            return jsonify({"error": "Number of values supplied({}) does not equal number of channels ({}).".format(len(values_list), len(channels_list))}, 404)

        this_fixture.set_channels(values_list)

    data = {
        "message": "Updated all selected fixtures."
    }
    return jsonify(data), 200

@routes.route('set_bpm/<string:bpm_0>/<string:bpm_1>', methods=['GET'])
def set_bpm(bpm_0: int, bpm_1: int):
    new_bpm = float(".".join([bpm_0, bpm_1]))

    current_app.parent.controller.ticker.set_bpm(new_bpm)

    data = {
        "message": "Set BPM to {}.".format(new_bpm)
    }
    return jsonify(data), 200

@routes.route('sync/<int:val>', methods=['GET'])
def sync(val: int):
    current_app.parent.controller.ticker.sync(val)

    data = {
        "message": "Synced to {} ms.".format(val)
    }
    return jsonify(data), 200

@routes.route('nudge/<string:val>', methods=['GET'])
def nudge(val: str):
    current_app.parent.controller.ticker.nudge(int(val))

    data = {
        "message": "Nudged animations by {} ms.".format(val)
    }
    return jsonify(data), 200

@routes.route('animations', methods=['GET'])
def animations():
    return render_template("animations.jinja2")