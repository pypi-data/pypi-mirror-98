# PYNWSSPC

This is a simple Python library designed to asyncronously retrieve data from the National Weather Service [Storm Prediction Center](https://www.spc.noaa.gov/). It provides several simple methods for determining the risk of a point, as well as more complex object storage for efficiently checking multiple locations.

## Classes

The following classes are available and in some cases dynamically created when retrieving data:

### Outlook

The Outlook class is for storing the data from a given SPC outlook. It requires an aiohttp `ClientSession`, the day for the outlook (1-8), and the type as a string (categorical, tornado, significant wind, etc.). See [the SPC website](https://www.spc.noaa.gov/misc/SPC_probotlk_info.html) for information on what types of outlooks they provide. 

Available types are `cat` (categorical), `hail` (hail), `sighail` (significant hail), `torn` (tornado), `sigtorn` (significant tornado), `wind` (wind), and `sigwind` (significant wind). 

### Day12Outlook

The Day12Outlook is for storing an entire set of Outlook objects for day 1 or day 2. The SPC day 1 and day 2 outlooks provide the same data, both categorical risk and probabilistic risk for each type of severe criteria. This class requires the day it is representing (either 1 or 2), and optionally it can be provided with an aiohttp `ClientSession` (required if using it standalone and updating from within the class) as well as the individual outlooks that make up the entire class.

When the Day12Outlook object is created, it either references the outlooks that were passed in, or creates new outlook objects to fill its data. It contains outlooks for categorical risk as well as all probabilistic categories. 

### Day3Outlook

The Day3Outlook is for storing an entire set of Outlook objects for day3. The SPC day 3 outlook provides only a categorical risk and overall probabilistic risk, including significant severe. Similarly to Day12Outlook, it can be provided with an aiohttp `ClientSession` (required if using it standalone and updating from within the class) as well as the individual outlooks that make up the class.

When the Day3Outlook object is created, it either references the outlooks that were passed in, or creates new outlook objects to fill its data. It contains outlooks for categorical risk, probabilistic risk, and significant severe probabilistic risk.

### RiskLevel

This is a basic class to store each type of risk level. It contains variables for each type of outlook, see above for syntax.

### Location

The Location class is to store and determine risk levels for the entire forecast period at a given location. It requires a latitude and longitude, then optionally can take an aiohttp `ClientSession` (required if using it standalone and updating from within the class) as well as outlook objects for various days. 

When the Location object is created, it contains references to two `Day12Outlook` objects, one for day 1 and one for day 2, as well as one `Day3Outlook` object, and four `Outlook` objects, one each for days 4 through 8. It also contains eight `RiskLevel` objects, one for each day. If the above objects are not passed in, they will be dynamically created. Then the various Outlook objects are subscribed to, and they call an internal update method within the Location class when they are updated. The internal update method uses the `determine_point_risk` method to determine the risk level at the defined point.

If using the Location class standalone, the `full_update()` and `day_update(day)` methods can be used to update the corresponding outlooks. These methods call the update method on the respective outlooks, which then call the internal update method on the Location object to update the point risk. `day_update(day)` requires the day that you wish to update, 1-8. 

## Methods

The library also contains the following methods for simple usage. 

### determine_point_risk(outlook, point)

This method requires an `Outlook` object and a shapely.geometry `Point` object. It will then determine the risk level for that point within the given `Outlook`. Note that the SPC GEOJSON returns in the `[long, lat]` format, so the `Point` requires that order as well.

### get_risk(session, day, type, point)

This method is probably the simplest way to use the library. It requires an aiohttp `ClientSession`, the day and type for the outlook (see above in the `Outlook` object for options), and a shapely.geometry `Point`. It then retrieves the requested outlook and determines the risk for the given point. Note that the SPC GEOJSON returns in the `[long, lat]` format, so the `Point` requires that order as well.


### get_highest_risk(session, day, type, outlook)

This method will determine the highest risk present in a given outlook. There are two options to use it, either by passing in an aiohttp `ClientSession`, or by passing in an `Outlook` object. If passing in a `ClientSession`, `day` and `type` can be specified. They default to day 1 and categorical. If passing in an `Outlook` object, none of the other options are required and are ignored. This returns the highest risk level that exists anywhere within the outlook. 

## Usage

Basic highest risk determination:
```
import asyncio

from aiohttp import ClientSession

from pynwsspc import get_highest_risk

async def main():
  async with ClientSession() as session:
    risk = await get_highest_risk(session, 2, "torn")
    print(risk)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

Basic location risk determination:
```
import asyncio

from aiohttp import ClientSession
from shapely.geometry import Point

from pynwsspc import get_risk

lat = 32.08
long = -81.09

point = Point(long, lat)

async def main():
  async with ClientSession() as session:
    risk = await get_risk(session, 1, "cat", point)
    print(risk)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

Basic location usage:
```
import asyncio

from aiohttp import ClientSession

from pynwsspc import Location

lat = 32.08
long = -81.09

async def main():
  async with ClientSession() as session:
    risk = Location(lat, long, session)
    await risk.full_update()
    print(risk.day1.sigtorn)
    print(risk.day3.prob)
    print(risk.day4.cat)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

Complex example with stored outlooks:
```
import asyncio

import pynwsspc

from aiohttp import ClientSession

lat1 = 32.08
long1 = -81.09

lat2 = 33.75
long2 = -84.39

async def main():
    async with ClientSession() as session:
        day1otk = pynwsspc.Day12Outlook(1, session)
        day2otk = pynwsspc.Day12Outlook(2, session)
        day3otk = pynwsspc.Day3Outlook(session)
        day4otk = pynwsspc.Outlook(4, session)
        day5otk = pynwsspc.Outlook(5, session)
        day6otk = pynwsspc.Outlook(6, session)
        day7otk = pynwsspc.Outlook(7, session)
        day8otk = pynwsspc.Outlook(8, session)
        outlooks = [day1otk, day2otk, day3otk, day4otk, 
                    day5otk, day6otk, day7otk, day8otk]

        loc1 = pynwsspc.Location(lat1, long1, None, day1otk, day2otk, day3otk,
                            day4otk, day5otk, day6otk, day7otk, day8otk)

        loc2 = pynwsspc.Location(lat2, long2, None, day1otk, day2otk, day3otk,
                            day4otk, day5otk, day6otk, day7otk, day8otk)

        # these will return None as the data has not been retrieved yet
        print(loc1.day1.cat)
        print(loc2.day2.sigtorn)
        for outlook in outlooks:
          await outlook.update()

        # these will now have the correct values
        print(loc1.day1.cat)
        print(loc2.day2.sigtorn)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```