# JFW-Encoder-Decoder
## A simple encoding/decoding scheme that freakin works

[![Build Status](https://travis-ci.org/heezes/jfw-encoding-decoding.svg?branch=main)](https://travis-ci.org/heezes)

This sdk is inspired from googles protocol buffers
This sdk is aimed to help embedded developer better integrate data exchange protocols with web/app developers. Data is encoded in binary format(Size and Speed advantage) and decoded into json format(Easy for web/app developer)
User decides the data format by providing a header file. The user can insert data members within the fundamental data structures. Which are:
>- veryHighPriorityData_t
>- highPriorityData_t
>- normalPriorityData_t
>- lowPriorityData_t
>- veryLowPriorityData_t

The structure names are to help user sort data members when using this sdk for data logging purpose.

- ✨Magic ✨

## Packet Structure

Data is encoded according to the following scheme
| SYNC_CHAR_1 | SYNC_CHAR_2 | LENGTH | MSG_ID | DATA[LENGTH] | CK_A | CK_B|
| ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| 0xB5 | 0x62 | Length | Packet Id | Length bytes of data | [Checksum] | [Checksum] |

## Features

- Data packetization for proper synchronization incase of garbage data.
- Checksum for data integrity
- Large range of fundamental c datatypes for code optimization
- Small code footprint and time complexity
- No dynamic allocation for C

Future Plans for development
> Add option for encryption
> Add support for other languages
> Test and Build enviroment

Currently only C and Python are supported

## Tech

- Currently the sdk does not uses any external dependency for C (except configuration file).
- The python dependencies are packed within the pypi package.

## Installation

SDK requires [Python] 3.6+ to run.

Install the package.

```sh
pip3 install jfwEncoderDecoder
```

Generate the strcture class from conf header file
```sh
python3 -m jfwEncoderDecoder.jfw_generator $filepath
```
Now the class file has been generated and user can start using the sdk

## Usage

Decoding
```sh
import json
import jfwEncoderDecoder.jfw_deserializer as jfw

binaryFilePath = "3014693-893931545-540029520-3732.bin"
with open(binaryFilePath, "rb") as f:
     data = f.read()
     ser = jfw.deserializer(data, len(data))
     ser.search()
     temp = list()
     while(ser.decode_idx < len(ser.sync_char_off)):
         final_json = ser.decode(False)
         if(final_json != None):
             temp.append(json.loads(final_json))
 print("Data Lost: "+ser.loss())
```

Encoding/Decoding
```sh
with open('file.json', "rb+") as f:
    lines = f.readlines()
    idx = 0
    for line in lines:
        idx += 1
        final_dictionary = json.loads(line)
        encoder = jfwEncoderDecoder.jfw_serializer.serializer(final_dictionary, len(final_dictionary))
        pkt_data = encoder.encode()
        decoder = jfwEncoderDecoder.jfw_deserializer.deserializer(pkt_data, len(pkt_data))
        decoder.search()
        ret_json = decoder.decode()
        if(json.dumps(final_dictionary) == str(ret_json)):
            print("Line "+str(idx)+": Encoding/Decoding Successful!")
        else:
            print("ERROR!!!!!!")
```

## Development

Want to contribute? Great!
Contact at altamash.ar96@gmail.com

## License

GNU General Public License v3 (GPLv3)

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
   [Checksum]: <https://en.wikipedia.org/wiki/Fletcher%27s_checksum#Example_calculation_of_the_Fletcher-16_checksum>
   [Python]: <https://www.python.org>