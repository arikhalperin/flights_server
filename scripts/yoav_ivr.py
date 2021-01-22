import os, sys, time, requests, json, io
from datetime import datetime
import freeswitch, threading, requests

# from freeswitch import *

RECORDINGS_DIRECTORY = "/opt/recordings/"
ts = time.time()


def do_http_upload(upload_url, file_path, data=None):
    freeswitch.consoleLog("crit", "do_http_upload-1")

    files = [('recording', open(file_path, 'rb'))]
    freeswitch.consoleLog("crit", "do_http_upload0")

    payload = {"interaction_type": "voice"}

    if data is not None:
        payload["data"] = data

    response = requests.request("POST", upload_url, files=files, params=payload)
    freeswitch.consoleLog("crit", "got server response")
    if response.status_code == 200:
        response = response.json()
        return response


def stop_recording(session):
    session.execute('stop_record_session',
                    RECORDINGS_DIRECTORY + "/" + session.getVariable('uuid') + "/" + session.getVariable(
                        "caller_id_number") + ".wav")


def start_recording(session):
    session.execute('set', 'RECORD_STEREO=false')
    session.execute('record_session',
                    RECORDINGS_DIRECTORY + "/" + session.getVariable('uuid') + "/" + session.getVariable(
                        "caller_id_number") + ".wav")


def handler(session, args):
    freeswitch.consoleLog("crit", "Handling IVR")
    session.setHangupHook(hangup_hook)

    record_message(session)

    session.hangup()
    freeswitch.consoleLog("crit", "Hung up")

    return "true"


def get_data(session, current_response):
    message = "message"

    if current_response["status"] != "more_data":
        return current_response["status"]

    if current_response["next"] == "origin":
        session.execute('playback', "/usr/share/freeswitch/sounds/origin.wav")
    if current_response["next"] == "destination":
        session.execute('playback', "/usr/share/freeswitch/sounds/destination.wav")
    if current_response["next"] == "travel_date":
        session.execute('playback', "/usr/share/freeswitch/sounds/travel_date.wav")
    if current_response["next"] == "capacity":
        session.execute('playback', "/usr/share/freeswitch/sounds/passengers.wav")
    if current_response["next"] == "user_id":
        session.execute('playback', "/usr/share/freeswitch/sounds/user_id.wav")

    start_recording(session)

    count = 100
    in_result = session.getDigits(1, "#", 400000)
    freeswitch.consoleLog("crit", "before loop")

    while in_result != "" and count > 0:
        freeswitch.consoleLog("crit", "In loop")
        in_result = session.getDigits(1, "#", 400000)
        count = count - 1

    stop_recording(session)
    filename = RECORDINGS_DIRECTORY + "/" + session.getVariable('uuid') + "/" + session.getVariable(
        "caller_id_number") + ".wav"
    if count > 0:
        result = do_http_upload("http://46.101.50.94:5000/v1/upload", filename, json.dumps(current_response["data"]))
        return get_data(session, result)


def record_message(session):
    count = 100
    freeswitch.consoleLog("crit", "Recording english")
    session.setVariable("RECORDING_LANGUAGE", "english")
    session.setVariable("RECORD_READ_ONLY", "true")
    start_recording(session)
    session.execute('playback', "/usr/share/freeswitch/sounds/yoav_greeting.wav")

    in_result = session.getDigits(1, "#", 400000)
    freeswitch.consoleLog("crit", "before loop")

    while in_result != "" and count > 0:
        freeswitch.consoleLog("crit", "In loop")
        in_result = session.getDigits(1, "#", 400000)
        count = count - 1

    stop_recording(session)
    filename = RECORDINGS_DIRECTORY + "/" + session.getVariable('uuid') + "/" + session.getVariable(
        "caller_id_number") + ".wav"
    result = do_http_upload("http://46.101.50.94:5000/v1/upload", filename)

    answer =get_data(session, result)

    if answer["status"]=="OK":
        session.execute('playback', "/usr/share/freeswitch/sounds/yoav_goodbye.wav")
    else:
        session.execute('playback', "/usr/share/freeswitch/sounds/error.wav")



def hangup_hook(session, what, args=''):
    freeswitch.consoleLog("crit", "Finished call 1")
    freeswitch.consoleLog("crit", "Finished call 2")
    freeswitch.consoleLog("crit", "Finished call 3")



