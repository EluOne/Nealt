Nealt
=====

Nova Echo Audit Log Tool

A command line tool created by me as the predecessor to Nesi and Nema. It is an application to interpret the output of audit logs produced by the game "Eve Online" by CCP Games, into something more usable by mining directors and production managers.
Currently audit logs have to be manually created by copy and pasting the log window out of game into a text file. There is API access to the logs, but it only gives limited history to work with and my directors prefer monthly stats.

At present it is a single window application which will output the data from a single log file selected by the user.

Currently this output groups by pilot and ore type, then outputs the fleet percentages of volume mined.
Salvaged materials and everything else not ice or ore currently dumps into their own sections only grouped by pilot.
