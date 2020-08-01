#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
This file contains the functionality for converting to and from the 
recursive-month calendaring format.  Timezones don't exist to this system,
nor does daylight savings, although those things may be implemented later.
"""

import datetime
import re

MONTHS = {
		'January':     ['Jan', 31],
		'February':    ['Feb', 28],
		'March':       ['Mar', 31],
		'April':       ['Apr', 30],
		'May':         ['May', 31],
		'June':        ['Jun', 30],
		'July':        ['Jul', 31],
		'August':      ['Aug', 31],
		'September':   ['Sep', 30],
		'October':     ['Oct', 31],
		'November':    ['Nov', 30],
		'December':    ['Dec', 31]
	}
REG_REGEX = re.compile(r"^\d{4}-((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-?)+$")
ISO_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}$")


def which_month_is_it(month):
	"""
	Handles number-to-month and month-to-number conversions.

	If given a string, returns a number; if given a number, returns
	a string (short version).
	"""

	if isinstance(month, int):
		try:
			return list(MONTHS.values())[month - 1][0]
		except IndexError:
			# no such month!  return None is at the end.
			pass

	elif isinstance(month, str):
		for i in range(12):
			if list(MONTHS.values())[i][0].startswith(month):
				return i + 1
	return None


def sanity_check_rti(date):
	"""
	Sanity-checks a value for a recursive-to-iso conversion.
	Returns either true or false, whether or not the date is
	safe to be passed to the `from_recursive_to_iso` function.
	Designed to be as un-crashable as possible.
	"""
	# Since we're not charged with figuring out *why*
	# a value doesn't work, the easiest (least typing)
	# method of doing this is to wrap a giant try-catch
	# for AssertionErrors and assert our way through the list
	# of requirements for that function, simply returning whether
	# or not we got to the end of the try block successfully.
	try:
		assert date, "Must enter a value!"
		assert isinstance(date, str), "Must be string type!"
		assert REG_REGEX.match(date), "Doesn't look like a recurdate!"

		# Looks good!
		return True
	except AssertionError as e:
		# This ain't it, chief.
		return False
	except Exception as e:
		# Jeez, something went really wrong.  Probably
		# should report this.
		raise


def sanity_check_itr(date):
	"""
	The reverse of `sanity_check_itr`.  Makes sure that a given
	argument is safe to pass into the `from_iso_to_recursive`
	function.
	Again, designed to be ultra-crash proof.
	"""
	# Just like last time.  Giant try-except asserting our way
	# through the list of requirements.
	try:
		assert date, "Must enter a value!"
		assert isinstance(date, str), "Must be a string!"
		assert ISO_REGEX.match(date), "Doesn't look like an isodate!"
		assert datetime.datetime.fromisoformat(date), "Couldn't convert!"

		# Ok, done here!
		return True
	except AssertionError as e:
		# Nope.
		return False
	except Exception:
		raise


def from_recursive_to_iso(date):
	"""
	Converts from a recursive calendar string to an ISO standard datetime.
	"""
	if not sanity_check_rti(date):
		# Make sure we can operate safely first.
		return ""

	months = date.split('-')
	assert len(months) >= 1, "you must specify at least one item in" \
		"your calendar!"

	year = int(months[0])
	months = months[1:]

	
	hours_total = 0
	depth = 0
	for month in months:
		hours_per_month_this_level = 730 / (12 ** depth)
		n_months_this_level = which_month_is_it(month) - 1
		hours_this_level = hours_per_month_this_level * \
				n_months_this_level
		hours_total += hours_this_level
		depth += 1
	
	iso = '{:04d}-01-01'.format(year)
	dt = datetime.datetime.fromisoformat(iso)
	dtime = datetime.timedelta(hours=hours_total)
	newdate = dt + dtime
	return newdate.isoformat()


def from_iso_to_recursive(date, max_depth=7):
	"""
	Converts from ISO standard datetime string to recursive calendar.
	"""
	if not sanity_check_itr(date):
		# Can't do it, no point trying.
		return ""

	dt = datetime.datetime.fromisoformat(date)
	iso2 = '{:04d}-01-01'.format(dt.year)
	base = datetime.datetime.fromisoformat(iso2)

	recursdate = '{:04d}'.format(dt.year)
	hours_remaining = (dt - base).total_seconds() / 3600
	depth = 0
	
	while hours_remaining:
		if depth > max_depth:
			break

		hours_per_month_this_level = 730 / (12 ** depth)
		n_months, hours_remaining = divmod(
				hours_remaining,
				hours_per_month_this_level
			)
		n_months = int(n_months) + 1
		new_month = which_month_is_it(n_months)
		recursdate = recursdate + '-' + new_month
		depth += 1

	return recursdate

