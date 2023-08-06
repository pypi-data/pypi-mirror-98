# Store the version here so:
# 1) we don't load dependencies by storing it in __init__.py
# 2) we can import it in setup.py for the same reason
# 3) we can import it into your module module
# 0.7.4 - Correct class declaration to include object
# 0.7.5 - Added an alias for streamid to IEAN
# 0.7.6 - Added repr function to SimpleEthernet
# 0.8.0 - Lots of updates and documentation updates
# 0.8.1 - Added IENA-N and IENA-D packets
# 0.9.0 - Added NDP
# 0.9.2 - Added Ch10
# 0.9.4 - Previous chapter 10 was the UDP wrapper. Correct Chapter10 packet now added
# 0.9.5 - Added ARINC data packet
# 0.10.0 - Added iNET
# 0.10.1 - Added info to exception
# 0.10.2 - Fixed IP checksum bug
# 0.11.0 - Chapter10 endianness changes
# 0.11.1 - IENA-N and IENA-D throw exception if there are not integer number of D and N parameters in the payload
# 0.11.2 - ParserAligned throws exception if the number of quadbytes is illegal
# 0.12.0 - Added IENA-M and IENA-Q
# 0.12.1 - Changed pcap to an iterator model
# 0.12.2 - Fixed iNET byte order
# 0.12.3 - Fixed iNET byte order
# 0.12.4 - Changed INET to separate seconds and nanoseconds
# 0.13.0 - Added UART Payload for Chapter 10
# 0.13.1 - Bug fixes on UART for Chapter 10
# 0.13.2 - Added NPD Segments for RS232
# 0.13.3 - Parser aligned printout
# 0.14.0 - Made compatiable with python3
# 0.15.0 - Added ch7 and updated all unit test to pass in both py3 py2
# 0.15.1 - Added unpack to ParserAligned
# 0.15.2 - Fixd the ascii example
# 0.15.3 - Minor updates to Ch7 and unittest
# 0.15.4 - Pcap comment removal
# 0.15.5 - Handled padding for UART data words in chapter 10
# 0.15.6 - Optimisations on Golay encoding
__version__ = '0.15.6'
