import datetime


def divide_sessions_by_id(snapshots):
    """
    Divides snapshots into sessions, segmented whenever the session ID changed
    :param snapshots: list of snapshots
    :type snapshots: list
    :return: list of sessions, where each session is a list of snapshots
    """
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


def divide_sessions_by_time(snapshots, idle_time):
    """
    Divides snapshots into sessions, segmented by idle time since last snapshot.
    :param snapshots: list of snapshots
    :param idle_time: list
    :type idle_time: datetime.timedelta
    :return: list of sessions, where each session is a list of snapshots
    """
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


def divide_sessions(snapshots, idle_time=datetime.timedelta(hours=2)):
    return divide_sessions_by_time(snapshots, idle_time)


def print_session_summary(library, idle_time=None):
    """
    Prints out a summary table of all the individual sessions in the given library.
    Default behavior is to print out the table based on whatever sessions are already stored in the library.

    If the idle_time parameter is specified, it will re-segment all the sessions with the given time,
    overwriting the previous session data.

    :param library:
    :param idle_time:
    :type idle_time: datetime.timedelta
    :return:
    """
    if idle_time:
        library.divide_sessions(idle_time)

    sessions = []

    for p in library.all_projects():
        sessions.extend(p.sessions)

    user_name_max = max([len(s[0].user_name) for s in sessions])
    project_name_max = max([len(s[0].project_name) for s in sessions])

    print("User Name".ljust(user_name_max) + "  " + "Project Name".ljust(project_name_max) + "  " +
          "First Date".center(26) + "  " + "Last Date".center(26) + "  " + "Time Period")
    for s in sessions:
        print(s[0].user_name.ljust(user_name_max) + "  " + s[0].project_name.ljust(project_name_max) + "  " +
              str(s[0].date) + "  " + str(s[-1].date) + "  " + str(s[-1].date - s[0].date))
