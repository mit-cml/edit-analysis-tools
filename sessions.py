import aiatools
import datetime


def divide_sessions_by_id(snapshots):
    """returns an array of sessions, where each session is an array of snapshots"""
    current_id = snapshots[0].session_id
    sessions = []
    current_session = []

    for s in snapshots:
        if s.session_id == current_id:
            current_session.append(s)
        else:
            sessions.append(current_session)
            current_session = [s]
            current_id = s.session_id

    sessions.append(current_session)

    return sessions


def divide_sessions_by_time(snapshots):
    idle_time = datetime.timedelta(hours=2)
    sessions = []
    current_session = []

    for s in snapshots:
        if s.delta < idle_time:
            current_session.append(s)
        else:
            sessions.append(current_session)
            current_session = [s]

    sessions.append(current_session)

    return sessions


def divide_sessions(snapshots):
    return divide_sessions_by_time(snapshots)
