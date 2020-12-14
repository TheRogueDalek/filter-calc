# filter-calc
Determine the best component values for a high-pass and low-pass ideal buffered cascaded filter, given a desired center frequency. Designed for Fall 2020 ECSE 2010 Omega Lab

This program will allow an user to input a desired center frequency, and later a configuration file with available component choices, to design cascaded high-pass and low-pass filters that admit the desired frequency.

As of this writing (13 Dec 2020), the program assumes that the user can insert voltage followers between filters to have a simple cascading behavior. Future improvements will allow for filter designs that do not require buffers in-between stages