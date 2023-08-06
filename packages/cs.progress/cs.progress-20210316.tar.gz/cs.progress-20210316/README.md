A progress tracker with methods for throughput, ETA and update notification;
also a compound progress meter composed from other progress meters.

*Latest release 20210316*:
* Progress.iterbar: only update the status line once per iteration, either before or after the yield according to incfirst.
* Progress.iterbar: fix the meaning of update_frequency to count iterations, add update_min_size to count progress advance.

## Function `auto_progressbar(*da, **dkw)`

Decorator for a function accepting an optional `progress`
keyword parameter.
If `progress` is `None` and the default `Upd` is not disabled,
run the function with a progress bar.

## Class `BaseProgress`

The base class for `Progress` and `OverProcess`
with various common methods.

Note that durations are in seconds
and that absolute time is in seconds since the UNIX epoch
(the basis of `time.time()`).

### Method `BaseProgress.__init__(self, name=None, start_time=None, units_scale=None)`

Initialise a progress instance.

Parameters:
* `name`: optional name
* `start_time`: optional UNIX epoch start time, default from `time.time()`
* `units_scale`: a scale for use with `cs.units.transcribe`,
  default `BINARY_BYTES_SCALE`

### Method `BaseProgress.__eq__(self, other)`

A Progress is equal to another object `other`
if its position equals `int(other)`.

### Method `BaseProgress.__ge__(self, other, NotImplemented=NotImplemented)`

Return a >= b.  Computed by @total_ordering from (not a < b).

### Method `BaseProgress.__gt__(self, other, NotImplemented=NotImplemented)`

Return a > b.  Computed by @total_ordering from (not a < b) and (a != b).

### Method `BaseProgress.__int__(self)`

`int(Progress)` returns the current position.

### Method `BaseProgress.__le__(self, other, NotImplemented=NotImplemented)`

Return a <= b.  Computed by @total_ordering from (a < b) or (a == b).

### Method `BaseProgress.__lt__(self, other)`

A Progress is less then another object `other`
if its position is less than `int(other)`.

### Method `BaseProgress.arrow(self, width, no_padding=False)`

Construct a progress arrow representing completion
to fit in the specified `width`.

### Method `BaseProgress.bar(self, label=None, upd=None, proxy=None, statusfunc=None, width=None, window=None, report_print=None, insert_pos=1, deferred=False)`

A context manager to create and withdraw a progress bar.
It returns the `UpdProxy` which displays the progress bar.

Parameters:
* `label`: a label for the progress bar,
  default from `self.name`.
* `proxy`: an optional `UpdProxy` to display the progress bar
* `upd`: an optional `cs.upd.Upd` instance,
  used to produce the progress bar status line if not supplied.
  The default `upd` is `cs.upd.Upd()`
  which uses `sys.stderr` for display.
* `statusfunc`: an optional function to compute the progress bar text
  accepting `(self,label,width)`.
* `width`: an optional width expressioning how wide the progress bar
  text may be.
  The default comes from the `proxy.width` property.
* `window`: optional timeframe to define "recent" in seconds;
  if the default `statusfunc` (`Progress.status`) is used
  this is passed to it
* `report_print`: optional `print` compatible function
  with which to write a report on completion;
  this may also be a `bool`, which if true will use `Upd.print`
  in order to interoperate with `Upd`.
* `insert_pos`: where to insert the progress bar, default `1`
* `deferred`: optional flag; if true do not create the
  progress bar until the first update occurs.

Example use:

    # display progress reporting during upload_filename()
    # which updates the supplied Progress instance
    # during its operation
    P = Progress(name=label)
    with P.bar(report_print=True):
        upload_filename(src, progress=P)

### Property `BaseProgress.elapsed_time`

Time elapsed since `start_time`.

### Property `BaseProgress.eta`

The projected time of completion: now + `remaining_time`.

If `reamining_time` is `None`, this is also `None`.

### Method `BaseProgress.format_counter(self, value, scale=None, max_parts=2, sep=',')`

Format `value` accoridng to `scale` and `max_parts`
using `cs.units.transcribe`.

### Method `BaseProgress.iterbar(self, it, label=None, upd=None, proxy=None, itemlenfunc=None, statusfunc=None, incfirst=False, width=None, window=None, update_frequency=1, update_min_size=0, report_print=None)`

An iterable progress bar: a generator yielding values
from the iterable `it` while updating a progress bar.

Parameters:
* `it`: the iterable to consume and yield.
* `itemlenfunc`: an optional function returning the "size" of each item
  from `it`, used to advance `self.position`.
  The default is to assume a size of `1`.
  A convenient alternative choice may be the builtin function `len`.
* `incfirst`: whether to advance `self.position` before we
  `yield` an item from `it` or afterwards.
  This reflects whether it is considered that progress is
  made as items are obtained or only after items are processed
  by whatever is consuming this generator.
  The default is `False`, advancing after processing.
* `label`: a label for the progress bar,
  default from `self.name`.
* `width`: an optional width expressing how wide the progress bar
  text may be.
  The default comes from the `proxy.width` property.
* `window`: optional timeframe to define "recent" in seconds;
  if the default `statusfunc` (`Progress.status`) is used
  this is passed to it
* `statusfunc`: an optional function to compute the progress bar text
  accepting `(self,label,width)`.
* `proxy`: an optional proxy for displaying the progress bar,
  a callable accepting the result of `statusfunc`.
  The default is a `cs.upd.UpdProxy` created from `upd`,
  which inserts a progress bar above the main status line.
* `upd`: an optional `cs.upd.Upd` instance,
  used only to produce the default `proxy` if that is not supplied.
  The default `upd` is `cs.upd.Upd()`
  which uses `sys.stderr` for display.
* `update_frequency`: optional update frequency, default `1`;
  only update the progress bar after this many iterations,
  useful if the iteration rate is quite high
* `update_min_size`: optional update step size, default `0`;
  only update the progress bar after an advance of this many units,
  useful if the iteration size increment is quite small
* `report_print`: optional `print` compatible function
  with which to write a report on completion;
  this may also be a `bool`, which if true will use `Upd.print`
  in order to interoperate with `Upd`.

Example use:

    from cs.units import DECIMAL_SCALE
    rows = [some list of data]
    P = Progress(total=len(rows), units_scale=DECIMAL_SCALE)
    for row in P.iterbar(rows, incfirst=True):
        ... do something with each row ...

    f = open(data_filename, 'rb')
    datalen = os.stat(f).st_size
    def readfrom(f):
        while True:
            bs = f.read(65536)
            if not bs:
                break
            yield bs
    P = Progress(total=datalen)
    for bs in P.iterbar(readfrom(f), itemlenfunc=len):
        ... process the file data in bs ...

### Property `BaseProgress.ratio`

The fraction of progress completed: `(position-start)/(total-start)`.
Returns `None` if `total` is `None` or `total<=start`.

Example:

    >>> P = Progress()
     P.ratio
    >>> P.total = 16
    >>> P.ratio
    0.0
    >>> P.update(4)
    >>> P.ratio
    0.25

### Property `BaseProgress.remaining_time`

The projected time remaining to end
based on the `throughput` and `total`.

If `total` is `None`, this is `None`.

### Method `BaseProgress.status(self, label, width, window=None)`

A progress string of the form:
*label*`: `*pos*`/`*total*` ==>  ETA '*time*

Parameters:
* `label`: the label for the status line;
  if `None` use `self.name`
* `width`: the available width for the status line;
  if not an `int` use `width.width`
* `window`: optional timeframe to define "recent" in seconds,
  default : `5`

### Method `BaseProgress.text_pos_of_total(self, fmt=None, fmt_pos=None, fmt_total=None, pos_first=False)`

Return a "total:position" or "position/total" style progress string.

Parameters:
* `fmt`: format string interpolating `pos_text` and `total_text`.
  Default: `"{pos_text}/{total_text}"` if `pos_first`,
  otherwise `"{total_text}:{pos_text}"`
* `fmt_pos`: formatting function for `self.position`,
  default `self.format_counter`
* `fmt_total`: formatting function for `self.total`,
  default from `fmt_pos`
* `pos_first`: put the position first if true (default `False`),
  only consulted if `fmt` is `None`

### Property `BaseProgress.throughput`

The overall throughput: `self.throughput_overall()`.

By comparison,
the `Progress.throughput` property is `self.throughput_recent`
if the `throughput_window` is not `None`,
otherwise it falls back to `throughput_overall`.

### Method `BaseProgress.throughput_overall(self)`

The overall throughput from `start` to `position`
during `elapsed_time`.

### Method `BaseProgress.throughput_recent(self, time_window)`

The recent throughput. Implemented by subclasses.

## Class `CheckPoint(builtins.tuple)`

CheckPoint(time, position)

### Property `CheckPoint.position`

Alias for field number 1

### Property `CheckPoint.time`

Alias for field number 0

## Class `OverProgress(BaseProgress)`

A `Progress`-like class computed from a set of subsidiary `Progress`es.

AN OverProgress instance has an attribute ``notify_update`` which
is a set of callables.
Whenever the position of a subsidiary `Progress` is updated,
each of these will be called with the `Progress` instance and `None`.

Example:

    >>> P = OverProgress(name="over")
    >>> P1 = Progress(name="progress1", position=12)
    >>> P1.total = 100
    >>> P1.advance(7)
    >>> P2 = Progress(name="progress2", position=20)
    >>> P2.total = 50
    >>> P2.advance(9)
    >>> P.add(P1)
    >>> P.add(P2)
    >>> P1.total
    100
    >>> P2.total
    50
    >>> P.total
    150
    >>> P1.start
    12
    >>> P2.start
    20
    >>> P.start
    0
    >>> P1.position
    19
    >>> P2.position
    29
    >>> P.position
    16

### Method `OverProgress.add(self, subprogress)`

Add a subsidairy `Progress` to the contributing set.

### Property `OverProgress.eta`

The `eta` is the maximum of the subsidiary etas.

### Property `OverProgress.position`

The `position` is the sum off the subsidiary position offsets
from their respective starts.

### Method `OverProgress.remove(self, subprogress, accrue=False)`

Remove a subsidairy `Progress` from the contributing set.

### Property `OverProgress.start`

We always return a starting value of 0.

### Property `OverProgress.throughput`

The `throughput` is the sum of the subsidiary throughputs.

### Method `OverProgress.throughput_recent(self, time_window)`

The `throughput_recent` is the sum of the subsidiary throughput_recentss.

### Property `OverProgress.total`

The `total` is the sum of the subsidiary totals.

## Class `Progress(BaseProgress)`

A progress counter to track task completion with various utility methods.

Example:

    >>> P = Progress(name="example")
    >>> P                         #doctest: +ELLIPSIS
    Progress(name='example',start=0,position=0,start_time=...,throughput_window=None,total=None):[CheckPoint(time=..., position=0)]
    >>> P.advance(5)
    >>> P                         #doctest: +ELLIPSIS
    Progress(name='example',start=0,position=5,start_time=...,throughput_window=None,total=None):[CheckPoint(time=..., position=0), CheckPoint(time=..., position=5)]
    >>> P.total = 100
    >>> P                         #doctest: +ELLIPSIS
    Progress(name='example',start=0,position=5,start_time=...,throughput_window=None,total=100):[CheckPoint(time=..., position=0), CheckPoint(time=..., position=5)]

A Progress instance has an attribute ``notify_update`` which
is a set of callables. Whenever the position is updated, each
of these will be called with the `Progress` instance and the
latest `CheckPoint`.

`Progress` objects also make a small pretense of being an integer.
The expression `int(progress)` returns the current position,
and `+=` and `-=` adjust the position.

This is convenient for coding, but importantly it is also
useful for discretionary use of a Progress with some other
object.
If you want to make a lightweight `Progress` capable class
you can set a position attribute to an `int`
and manipulate it carefully using `+=` and `-=` entirely.
If you decide to incur the cost of maintaining a `Progress` object
you can slot it in:

    # initial setup with just an int
    my_thing.amount = 0

    # later, or on some option, use a Progress instance
    my_thing.amount = Progress(my_thing.amount)

### Method `Progress.__init__(self, position=None, name=None, start=None, start_time=None, throughput_window=None, total=None, units_scale=None)`

Initialise the Progesss object.

Parameters:
* `position`: initial position, default `0`.
* `name`: optional name for this instance.
* `start`: starting position of progress range,
  default from `position`.
* `start_time`: start time of the process, default now.
* `throughput_window`: length of throughput time window in seconds,
  default None.
* `total`: expected completion value, default None.

### Method `Progress.__iadd__(self, delta)`

Operator += form of advance().

>>> P = Progress()
>>> P.position
0
>>> P += 4
>>> P.position
4
>>> P += 4
>>> P.position
8

### Method `Progress.__isub__(self, delta)`

Operator -= form of advance().

>>> P = Progress()
>>> P.position
0
>>> P += 4
>>> P.position
4
>>> P -= 4
>>> P.position
0

### Method `Progress.advance(self, delta, update_time=None)`

Record more progress, return the advanced position.

>>> P = Progress()
>>> P.position
0
>>> P.advance(4)
>>> P.position
4
>>> P.advance(4)
>>> P.position
8

### Property `Progress.latest`

Latest datum.

### Property `Progress.position`

Latest position.

### Property `Progress.throughput`

Current throughput per second.

If `self.throughput_window` is not `None`,
calls `self.throughput_recent(throughput_window)`.
Otherwise call `self.throughput_overall()`.

### Method `Progress.throughput_recent(self, time_window)`

Recent throughput per second within a time window in seconds.

The time span overlapping the start of the window is included
on a flat pro rata basis.

### Property `Progress.total`

Return the current total.

### Method `Progress.update(self, new_position, update_time=None)`

Record more progress.

>>> P = Progress()
>>> P.position
0
>>> P.update(12)
>>> P.position
12

## Function `progressbar(it, label=None, position=None, total=None, units_scale=((0, ''),), **kw)`

Convenience function to construct and run a `Progress.iterbar`
wrapping the iterable `it`,
issuing and withdrawning a progress bar during the iteration.

Parameters:
* `it`: the iterable to consume
* `label`: optional label, doubles as the `Progress.name`
* `position`: optional starting position
* `total`: optional value for `Progress.total`,
  default from `len(it)` if supported.
* `units_scale`: optional units scale for `Progress`,
  default `UNSCALED_SCALE`

If `total` is `None` and `it` supports `len()`
then the `Progress.total` is set from it.

All arguments are passed through to `Progress.iterbar`.

Example use:

    for row in progressbar(rows):
        ... do something with row ...

## Function `selftest(argv)`

Exercise some of the functionality.

# Release Log



*Release 20210316*:
* Progress.iterbar: only update the status line once per iteration, either before or after the yield according to incfirst.
* Progress.iterbar: fix the meaning of update_frequency to count iterations, add update_min_size to count progress advance.

*Release 20210306*:
progressbar: accept new optional `position` parameter, used to initialise the Progress.

*Release 20201102.1*:
DISTINFO: fix module dependencies.

*Release 20201102*:
* Format/layout changes for the default status line.
* Progress.throughtput_recent: return None if no new positions beyond the starting position.
* BaseProgress.status: accept label=None (default to self.name) and width=UpdProxy (uses width.width).
* BaseProgress.status: new optional window parameter, default 5, defining the recent throughput window size in seconds.
* A few bugfixes.

*Release 20201025*:
* Some formatting improvements.
* BaseProgress.bar: new insert_pos parameter to position the progress bar, default still 1.
* BaseProgress.bar: new deferred parameter putting off the status bar until the first update.
* BaseProgress.bar: accept new optional `proxy` parameter to use (and not delete) an existing UpdProxy for display.
* Progress.text_pos_of_total: new `pos_first=False` parameter, rendering the total before the position by default (less progress bar noise).
* New @auto_progressbar decorator to provide a progress bar and initialise progress= parameter to functions which can use a Progress for reporting.
* Assorted fixes.

*Release 20200718.3*:
BaseProgress.bar, progressbar: new optional report_print parameter for reporting on completion.

*Release 20200718.2*:
Bugfix: BaseProgress.status: handle throughput=0 when total=None.

*Release 20200718.1*:
BaseProgress.bar, progressbar: new optional update_frequency parameter for less frequent updates.

*Release 20200718*:
* Readability improvement for default status line.
* progressbar: default units_scale=UNSCALED_SCALE.

*Release 20200716.1*:
BaseProgress.status: round throughput to an int if >=10.

*Release 20200716*:
* BaseProgress.status: distinguish "idle" (position >= total) from "stalled" (position < total).
* BaseProgress.status: make the status very short if the progress is idle.

*Release 20200627*:
* BaseProgress.status: handle throughput=None (before any activity).
* BaseProgress: drop count_of_total_bytes_text, superceded by format_counter (which honours the units_scale).

*Release 20200626*:
* New Progress.bar generator method iterating over an iterable while displaying a progress bar.
* New convenience function progressbar(it,...) which rolls its own Progress instance.
* Progress: always support a throughput window, default to DEFAULT_THROUGHPUT_WINDOW = 5s.
* Improve the default progress bar render returned by Progress.status().

*Release 20200613*:
* BaseProgress, Progress and OverProgress now accept an optional units_scale, such as cs.units.UNSCALED_SCALE, to use when expressing progress - the default remains BINARY_SCALE.
* New arrow(), format_counter() and text_pos_of_total() methods to produce components of the status string for tuning or external reuse.

*Release 20200520*:
OverProgress: throughput and eta implementations.

*Release 20200129.3*:
Test __version__ machinery again.

*Release 20200129.2*:
set __version__ to '20200129.2'

*Release 20200129.1*:
Dummy release to test new __version__.

*Release 20200129*:
New Progress.count_of_total_bytes_text property presenting "3kB/40MB" style text.

*Release 20190812*:
* New OverProgress class which is a composite of a set of subsidiary Progress instances.
* Assorted other small updates.

*Release 20190220*:
* Progress: be somewhat like an int.
* New status() method returning a convenient one line progress status report.

*Release 20180703.2*:
Progress: make .total into a property in order to fire the update notifications.

*Release 20180703.1*:
Progress: additions and changes to API: new .ratio, .elapsed_time, rename .projected to .remaining_time.

*Release 20180703*:
Initial release of cs.progress.
