# Recursive Months Calendar

This is a proof-of-concept implementation of a really, really
bad calendaring system.

Years are still unchanged, except there's no more such thing
as a leap year.  We disregard that extra day, nobody needs it.

The months of the year are roughly as normal, except that
instead of randomly arbitrated numbers of days each month
is *exactly* 1/12 of a year long, or 730 hours long.  This
fact will soon become important.

To handle dates within the months, we use ... more months.
Each month is broken up into twelve more months, each now
60.8333 hours long.  The sub-months use the same names as
the regular months.

This cycle of recursive months repeats until you get as
precise as you want to with youre date/time.  Time-of-day
as a separate item from date doesn't really exist in this
system, so times are specified as just more precise dates,
and dates are expressed as less precise times.

## Example

Converting 2020-01-01 00:01 to recursive months:

  1. Year is 2020, that part's easy
  2. First level of month: January
  3. Second level of month: last level had day 1, 1/31 = x/12, x=0.387
  4. Third level: last day was 0.387, 0.387/31 = x/12, x=0.149
  5.  and so on...

## Why?

Dunno.

## Should I use this?

Probably not.

