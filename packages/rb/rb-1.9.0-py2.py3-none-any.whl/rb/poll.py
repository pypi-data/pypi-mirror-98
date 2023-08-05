import fcntl
import array
import select
import termios


class BasePoller(object):
    is_available = False

    def __init__(self):
        self.objects = {}

    def register(self, key, f):
        self.objects[key] = f

    def unregister(self, key):
        return self.objects.pop(key, None)

    def poll(self, timeout=None):
        raise NotImplementedError()

    def get(self, key):
        return self.objects.get(key)

    def __len__(self):
        return len(self.objects)

    def __iter__(self):
        # Make a copy when iterating so that modifications to this object
        # are possible while we're going over it.
        return iter(self.objects.values())


class SelectPoller(BasePoller):
    is_available = hasattr(select, "select")

    def poll(self, timeout=None):
        objs = list(self.objects.values())
        rlist, wlist, xlist = select.select(objs, objs, [], timeout)
        if xlist:
            raise RuntimeError("Got unexpected OOB data")
        return [(x, "read") for x in rlist] + [(x, "write") for x in wlist]


class PollPoller(BasePoller):
    is_available = hasattr(select, "poll")

    def __init__(self):
        BasePoller.__init__(self)
        self.pollobj = select.poll()
        self.fd_to_object = {}

    def register(self, key, f):
        BasePoller.register(self, key, f)
        self.pollobj.register(
            f.fileno(), select.POLLIN | select.POLLOUT | select.POLLHUP
        )
        self.fd_to_object[f.fileno()] = f

    def unregister(self, key):
        rv = BasePoller.unregister(self, key)
        if rv is not None:
            self.pollobj.unregister(rv.fileno())
            self.fd_to_object.pop(rv.fileno(), None)
        return rv

    def poll(self, timeout=None):
        rv = []
        for fd, event in self.pollobj.poll(timeout):
            obj = self.fd_to_object[fd]
            if event & select.POLLIN:
                rv.append((obj, "read"))
            if event & select.POLLOUT:
                rv.append((obj, "write"))
            if event & select.POLLHUP:
                rv.append((obj, "close"))
        return rv


class KQueuePoller(BasePoller):
    is_available = hasattr(select, "kqueue")

    def __init__(self):
        BasePoller.__init__(self)
        self.kqueue = select.kqueue()
        self.events = []
        self.event_to_object = {}

    def register(self, key, f):
        BasePoller.register(self, key, f)
        r_event = select.kevent(
            f.fileno(),
            filter=select.KQ_FILTER_READ,
            flags=select.KQ_EV_ADD | select.KQ_EV_ENABLE,
        )
        self.events.append(r_event)
        w_event = select.kevent(
            f.fileno(),
            filter=select.KQ_FILTER_WRITE,
            flags=select.KQ_EV_ADD | select.KQ_EV_ENABLE,
        )
        self.events.append(w_event)
        self.event_to_object[f.fileno()] = f

    def unregister(self, key):
        rv = BasePoller.unregister(self, key)
        if rv is not None:
            fd = rv.fileno()
            self.events = [x for x in self.events if x.ident != fd]
            self.event_to_object.pop(fd, None)
        return rv

    def poll(self, timeout=None):
        events = self.kqueue.control(self.events, 128, timeout)
        rv = []
        for ev in events:
            obj = self.event_to_object.get(ev.ident)
            if obj is None:
                # It happens surprisingly frequently that kqueue returns
                # write events things no longer in the kqueue.  Not sure
                # why
                continue
            if ev.filter == select.KQ_FILTER_READ:
                rv.append((obj, "read"))
            elif ev.filter == select.KQ_FILTER_WRITE:
                rv.append((obj, "write"))
            if ev.flags & select.KQ_EV_EOF:
                rv.append((obj, "close"))
        return rv


class EpollPoller(BasePoller):
    is_available = hasattr(select, "epoll")

    def __init__(self):
        BasePoller.__init__(self)
        self.epoll = select.epoll()
        self.fd_to_object = {}

    def register(self, key, f):
        BasePoller.register(self, key, f)
        self.epoll.register(
            f.fileno(), select.EPOLLIN | select.EPOLLHUP | select.EPOLLOUT
        )
        self.fd_to_object[f.fileno()] = f

    def unregister(self, key):
        rv = BasePoller.unregister(self, key)
        if rv is not None:
            self.epoll.unregister(rv.fileno())
            self.fd_to_object.pop(rv.fileno(), None)
        return rv

    def poll(self, timeout=None):
        if timeout is None:
            timeout = -1
        rv = []
        for fd, event in self.epoll.poll(timeout):
            obj = self.fd_to_object[fd]
            if event & select.EPOLLIN:
                rv.append((obj, "read"))
            if event & select.EPOLLOUT:
                rv.append((obj, "write"))
            if event & select.EPOLLHUP:
                rv.append((obj, "close"))
        return rv


def _is_closed_select(f):
    rlist, wlist, _ = select.select([f], [f], [], 0.0)
    if not rlist and not wlist:
        return False
    buf = array.array("i", [0])
    fcntl.ioctl(f.fileno(), termios.FIONREAD, buf)
    return buf[0] == 0


def _is_closed_poll(f):
    poll = select.poll()
    poll.register(f.fileno(), select.POLLHUP)
    for _, event in poll.poll(0.0):
        if event == "close":
            return True
    return False


def _is_closed_kqueue(f):
    kqueue = select.kqueue()
    event = select.kevent(
        f.fileno(),
        filter=select.KQ_FILTER_READ,
        flags=select.KQ_EV_ADD | select.KQ_EV_ENABLE,
    )
    for event in kqueue.control([event], 128, 0.0):
        if event.flags & select.KQ_EV_EOF:
            return True
    return False


def is_closed(f):
    if KQueuePoller.is_available:
        return _is_closed_kqueue(f)
    if PollPoller.is_available:
        return _is_closed_poll(f)
    return _is_closed_select(f)


available_pollers = [
    poll
    for poll in [KQueuePoller, PollPoller, EpollPoller, SelectPoller]
    if poll.is_available
]
poll = available_pollers[0]
