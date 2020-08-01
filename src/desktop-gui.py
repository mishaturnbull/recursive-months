#!/bin/python3
# -*- coding: utf-8 -*-

"""
Desktop Tcl/Tk converter and clock for the recursive-months calendaring system.
Designed to make people as unhappy as possible.

+----------------------------------------------------------------------------+
| Recursive Months                                                     - o x |
| -------------------------------------------------------------------------- |
| Right now is 2020-07-31T21:50:20.500000                                    |
| which is 2020-Aug-Jan-Jan-Feb-Dec-Oct-Dec-Dec                              |
|                                                                            |
| Enter text in either box to convert a specific date/time:                  |
| ISO [2020-01-01T00:00:01.000000                                          ] |
| RCR [2020-Jan-Jan-Jan-Jan-Jan-Jan-Feb-Feb                                ] |
+----------------------------------------------------------------------------+
"""

import threading
import datetime
import time
import tkinter as tk
import conversions

UPDATE_LOOP_RATE_HZ = 2


class ClockUpdateWorker(threading.Thread):
	"""
	Handles updating of the clock fields in the GUI from the background
	so the GUI doesn't lag or freeze.
	"""

	def __init__(self, handler):
		"""
		Bind to the GUI, and super-init the Thread class.
		"""
		threading.Thread.__init__(self)
		self.handler = handler
		self.exit = False
		self.stoprequest = threading.Event()
		self.pausetime = 1 / UPDATE_LOOP_RATE_HZ
	
	def run(self):
		"""
		Run the clock updater.
		"""
		try:
			while not self.stoprequest.isSet():
				# grab time in ISO and recursive format
				now_iso = datetime.datetime.now().isoformat()
				now_rcr = conversions.from_iso_to_recursive(
						now_iso
					)

				# push new time to display
				self.handler.lbl_iso.config(text=now_iso)
				self.handler.lbl_rcr.config(text=now_rcr)

				# delay for the requested refresh rate
				time.sleep(self.pausetime)
		except RuntimeError as e:
			# RuntimeErrors in a thread run method most often mean
			# that we're no longer in the main loop (i.e. the
			# parent program has terminated).  Safest way to handle
			# this is to also exit the child thread
			self.stoprequest.set()
			return
	
	def join(self, timeout=None):
		self.stoprequest.set()
		super(ClockUpdateWorker, self).join(timeout)

class GUIRoot(object):

	"""
	Base object for the converter/clock for the bad calendar system.
	"""

	def __init__(self):
		"""
		Start making people mad.
		"""
		self.root = tk.Tk()

		# set window basics
		self.root.title('Recursive Months')
		# bind the close command to also close the child update thread
		self.root.protocol('WM_DELETE_WINDOW', self.close)

		# Start building the GUI
		self.lbl_iso = tk.Label(self.root, text='ISO date placeholder')
		self.lbl_iso.grid(row=0, column=0, sticky='nw')
		self.lbl_rcr = tk.Label(self.root, text='RCR date placeholder')
		self.lbl_rcr.grid(row=1, column=0, sticky='nw')
		
		# have to add an empty label here to force tk to put a blank
		# space in a row
		tk.Label(self.root, text=' ').grid(row=2, column=0, sticky='w')
		tk.Label(self.root, text=''
			'Enter text in either box to convert a specific '
			'date/time:') \
			.grid(row=3, column=0, sticky='nw')
		
		# bind a new thread to this instance as a handler
		self.thread = ClockUpdateWorker(self)

	def go(self):
		"""
		Starts the GUI!
		"""
		self.thread.start()
		self.root.mainloop()

	def close(self):
		"""
		Close method override to handle termination of the child
		thread as well as the GUi object.
		"""
		self.thread.stoprequest.set()
		self.root.destroy()


if __name__ == '__main__':
	GUIRoot().go()


