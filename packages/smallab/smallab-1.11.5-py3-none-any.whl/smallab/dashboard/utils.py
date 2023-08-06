from queue import Full

from smallab.dashboard.dashboard_events import LogEvent


class LogToEventQueue:
    """A file-like object that writes to the event queue.
     This is used so that logs will get added to the event queue to be displayed by the dashboard"""
    def __init__(self,eventQueue):
        self.eventQueue = eventQueue

    def write(self, t):
        put_in_event_queue(self.eventQueue,LogEvent(t))


    def flush(self):
        pass


def put_in_event_queue(eventQueue,o):
    '''
    This is just to put in the event queue without waiting or failing if it's full
    :param o:
    :return:
    '''
    try:
        eventQueue.put_nowait(o)
    except Full:
        pass
