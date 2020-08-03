# Recursive Months Calendar

This is a proof-of-concept implementation of a really, really
bad calendaring system.

Years are still unchanged, except there's no longer such a
thing as a leap year.  We disregard that extra day, nobody needs it.

The months of the year are roughly the same, except that
instead of a randomly arbitrated numbers of days each month
is *exactly* 1/12 of a year long-or 730 hours long.  This
fact will soon become important.

To handle dates within the months, we use ... more months.
Each month is then broken up into twelve more months, each now
being 60.8333 hours long.  The sub-months use the same names as
the regular months.

This cycle of recursive months repeats until you get as
precise as you want to with youre date/time.  Time-of-day
as a separate item from date doesn't really exist in this
system, so times are specified as just more precise dates,
and dates are expressed as less precise times.

## Example

Converting 2020-Aug-Oct-May-Jun-Apr-Feb-Jun-Oct to regular
date format:

1. Year is 2020.
2. Month is August.
3. Divide 10 (Oct) by 12, add that * 730^-1 hours to the start
   of August 2020.
4. Divide 5 (May) by 12, add that * 730^-2 hours to the cumulative
   total.
5. Divide 6 (Jun) by 12, add that * 730^-3 hours to the cumulative
   total.

Repeat until you've exhausted the string of months, then convert
the cumulative total plus August 2020 to an ISO date.  Done!
Easy, right?

## FAQ's

### Why?

Dunno.

### Should I use this?

Probably not.

## Reviews from happy users!

*Why would anyone want to do this?*  
-My mom

*Hahahahahahahaha!!!*  
-Coworker/friend

*I hate you.*  
-My roommate

