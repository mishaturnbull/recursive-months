#!/usr/env/python3
# -*- coding: utf-8 -*-

"""
This file contains the functionality for converting to and from the 
recursive-month calendaring format.  Timezones don't exist to this system,
nor does daylight savings, although those things may be implemented later.
"""

import datetime

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


def from_recursive_to_iso(date):
	"""
	Converts from a recursive calendar string to an ISO standard datetime.
	"""
	if not isinstance(date, str):
		return False

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

	try:
		dt = datetime.datetime.fromisoformat(date)
	except Exception:
		return "Nope"

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

