# MongoDataRandomizer

This is a simple data randomizer to load up a MongoDB database with data. It supports two document types: a generic patient data document and a geographic document.

## Installation
### From PyPI
* `pip install MongoRandomizer`

### From Source
* Download source code
* `cd` to the download directory
* Run `pip install --editable .`

## Use
### Help
```
graboskycMBP:~ graboskyc$ MongoRandomizer -h
usage: MongoRandomizer [-h] [-c CS] [-t T] [-b B] [-m M] [-p P] [-w WC] [-j]
                       [-g]
                       task

CLI Tool for continually writing random data to a MongoDB database for testing
purposes

positional arguments:
  task              clean, insert, insertAndUpdate, read, everything

optional arguments:
  -h, --help        show this help message and exit
  -c CS             server connection string
  -t T              threads to use, if left off, use 10
  -b B              blocksize to use. if not inclided, use 1000
  -m M              max blocks to use. if not inclided, use 1000
  -p P              additional chars of padding to increase document size
  -w WC             write concern to use. if blank, none used
  -j, --journaling  if omitted, false. if flag enabled, journal
  -g, --geo         if omitted, use customer data. if flag enabled push
                    geographic data
  ```

### Random Inserts

```
graboskycMBP:~ graboskyc$ MongoRandomizer -c mongodb://localhost -t 5 -b 500 -p 10 -w 1 -j insert

About to enter data in: 
	Threads: 5
	DB: demodb
	Collection: democollection
	Blocksize: 1000
	Max Blocks: 500
	Write Concern: 1
	Journaling: True

This process will continue until you press control+c or break
```

### Sample Document
```
{
	"_id" : ObjectId("5b7db58ecc39345cebc78f67"),
	"prescriptions" : [
		"Drug water adult.",
		"Enjoy month.",
		"Just always wind summer.",
		"Bad street me.",
		"Assume.",
		"Section.",
		"Forward nearly.",
		"Town community boy.",
		"Vote major.",
		"Walk.",
		"Left night receive.",
		"Relationship speak.",
		"Affect nearly.",
		"Present star special.",
		"Employee instead.",
		"Kid foot direction poor.",
		"Determine law."
	],
	"accountNumber" : 48,
	"padding" : "aaaaaaaaaa",
	"address" : "847 Ferguson Rd.",
	"payment" : 60,
	"occupation" : "Aid worker",
	"singupDate" : ISODate("2018-08-22T19:11:55.442Z"),
	"copay" : 20,
	"notes" : "Crime evening nation artist blue far fast generation. Play list range none before night everyone. Doctor make score around.",
	"zipcode" : "43418",
	"state" : "WY",
	"fullname" : "Donna Webster",
	"deductible" : 300
}
```

### Sample Geo Document
```
{
	"_id" : ObjectId("5b9fd129cc39341758236d80"),
	"padding" : "",
	"notes" : "Wait mean performance view billion plan civil this. Cup prevent season.\nEffect thought while get market war wife oil.",
	"name" : "Mr. Antonio Salas MD",
	"location" : {
		"type" : "Point",
		"coordinates" : [
			-73.59354663520122,
			42.00216814289992
		]
	}
}
```