import json

from aiohttp import ClientSession, ClientResponseError
from datetime import datetime, timedelta
from shapely.geometry import Point, shape

# day 1 times: 0600Z, 1300Z, 1630Z, 2000Z, and 0100Z
# day 2 times: 100 AM (CST and CDT) and 1730Z
# day 3 time: 230 AM (CST and CDT)
# day 4 - 8 time: 400 AM (CST and CDT)

def get_url(day, type):
    if day == 1 or day == 2:
        return "https://www.spc.noaa.gov/products/outlook/day%sotlk_%s.nolyr.geojson" % (day, type)
    if day == 3:
        return "https://www.spc.noaa.gov/products/outlook/day3otlk_%s.lyr.geojson" % (type)
    if day >= 4:
        return "https://www.spc.noaa.gov/products/exper/day4-8/day%sprob.nolyr.geojson" % (day)

class Event():
    pass

class Observable():
    def __init__(self):
        self._callbacks = []
    def subscribe(self, callback):
        self._callbacks.append(callback)
    def unsubscribe(self, callback):
        self._callbacks.remove(callback)
    async def fire(self, **attrs):
        e = Event()
        e.source = self
        for k, v in attrs.items():
            setattr(e, k, v)
        for callback in self._callbacks:
            await callback._update(e=e)
    

class Outlook(Observable):
    # Class for storing a SPC outlook
    def __init__(self, day, session: ClientSession, type=None):
        super().__init__()
        self.data = None
        self.type = type
        self.day = day
        self._url = get_url(self.day, self.type)
        self._session = session

    async def update(self):
        resp = await self._session.get(self._url)
        if resp.status == 200:
            data = await resp.read()
            data = json.loads(data)
        else:
            raise ClientResponseError(
                    resp.request_info,
                    resp.history
                    )

        self.data = data
        await self.fire(day=self.day)

class Day12Outlook(Observable):
    # Class for storing an entire set of day 1 or 2 outlooks
    def __init__(
        self,
        day,
        session: ClientSession=None,
        cat: Outlook=None,
        hail: Outlook=None,
        sighail: Outlook=None,
        torn: Outlook=None,
        sigtorn: Outlook=None,
        wind: Outlook=None,
        sigwind: Outlook=None
    ):
        super().__init__()
        self.session = session
        self.day = day
        self.cat = cat or Outlook(self.day, self.session, "cat")
        self.hail = hail or Outlook(self.day, self.session, "hail")
        self.sighail = sighail or Outlook(self.day, self.session, "sighail")
        self.torn = torn or Outlook(self.day, self.session, "torn")
        self.sigtorn = sigtorn or Outlook(self.day, self.session, "sigtorn")
        self.wind = wind or Outlook(self.day, self.session, "wind")
        self.sigwind = sigwind or Outlook(self.day, self.session, "sigwind")
        self.outlooks = [self.cat, self.hail, self.sighail, self.torn,
                            self.sigtorn, self.wind, self.sigwind]

    async def update(self):
        for outlook in self.outlooks:
            await outlook.update()
        await self.fire(day=self.day)

class Day3Outlook(Observable):
    # Class for storing an entire set of day 3 outlooks
    def __init__(
        self,
        session: ClientSession,
        cat: Outlook=None,
        prob: Outlook=None,
        sigprob: Outlook=None
    ):
        super().__init__()
        self.session = session
        self.cat = cat or Outlook(3, self.session, "cat")
        self.prob = prob or Outlook(3, self.session, "prob")
        self.sigprob = sigprob or Outlook(3, self.session, "sigprob")
        self.outlooks = [self.cat, self.prob, self.sigprob]

    async def update(self):
        for outlook in self.outlooks:
            await outlook.update()
        await self.fire(day=3)

class RiskLevel():
    # Class for storing different categories of risk levels
    def __init__(self):
        self.cat = None
        self.hail = None
        self.sighail = None
        self.torn = None
        self.sigtorn = None
        self.wind = None
        self.sigwind = None
        self.prob = None
        self.sigprob = None

class Location():
    # Class for storing data on a specific location and its risks
    def __init__(self,
                lat,
                long,
                session: ClientSession=None,
                day1otk=None,
                day2otk=None,
                day3otk=None,
                day4otk=None,
                day5otk=None,
                day6otk=None,
                day7otk=None,
                day8otk=None):
        self.session = session
        self.point = Point(long, lat)
        self.day1 = RiskLevel()
        self.day1otk = day1otk or Day12Outlook(1, session)
        self.day1otk.subscribe(self)
        self.day2 = RiskLevel()
        self.day2otk = day2otk or Day12Outlook(2, session)
        self.day2otk.subscribe(self)
        self.day3 = RiskLevel()
        self.day3otk = day3otk or Day3Outlook(session)
        self.day3otk.subscribe(self)
        self.day4 = RiskLevel()
        self.day4otk = day4otk or Outlook(4, session)
        self.day4otk.subscribe(self)
        self.day5 = RiskLevel()
        self.day5otk = day5otk or Outlook(5, session)
        self.day5otk.subscribe(self)
        self.day6 = RiskLevel()
        self.day6otk = day6otk or Outlook(6, session)
        self.day6otk.subscribe(self)
        self.day7 = RiskLevel()
        self.day7otk = day7otk or Outlook(7, session)
        self.day7otk.subscribe(self)
        self.day8 = RiskLevel()
        self.day8otk = day8otk or Outlook(8, session)
        self.day8otk.subscribe(self)

    async def _update(self, e: Event):
        if e.day == 1:
            self.day1.cat = determine_point_risk(self.day1otk.cat, self.point)
            self.day1.hail = determine_point_risk(self.day1otk.hail, self.point)
            self.day1.sighail = determine_point_risk(self.day1otk.sighail, self.point)
            self.day1.torn = determine_point_risk(self.day1otk.torn, self.point)
            self.day1.sigtorn = determine_point_risk(self.day1otk.sigtorn, self.point)
            self.day1.wind = determine_point_risk(self.day1otk.wind, self.point)
            self.day1.sigwind = determine_point_risk(self.day1otk.sigwind, self.point)

        if e.day == 2:
            self.day2.cat = determine_point_risk(self.day2otk.cat, self.point)
            self.day2.hail = determine_point_risk(self.day2otk.hail, self.point)
            self.day2.sighail = determine_point_risk(self.day2otk.sighail, self.point)
            self.day2.torn = determine_point_risk(self.day2otk.torn, self.point)
            self.day2.sigtorn = determine_point_risk(self.day2otk.sigtorn, self.point)
            self.day2.wind = determine_point_risk(self.day2otk.wind, self.point)
            self.day2.sigwind = determine_point_risk(self.day2otk.sigwind, self.point)

        if e.day == 3:
            self.day3.cat = determine_point_risk(self.day3otk.cat, self.point)
            self.day3.prob = determine_point_risk(self.day3otk.prob, self.point)
            self.day3.sigprob = determine_point_risk(self.day3otk.sigprob, self.point)

        if e.day == 4:
            self.day4.cat = determine_point_risk(self.day4otk, self.point)

        if e.day == 5:
            self.day5.cat = determine_point_risk(self.day5otk, self.point)

        if e.day == 6:
            self.day6.cat = determine_point_risk(self.day6otk, self.point)

        if e.day == 7:
            self.day7.cat = determine_point_risk(self.day7otk, self.point)

        if e.day == 8:
            self.day8.cat = determine_point_risk(self.day8otk, self.point)

    async def full_update(self):
        await self.day1otk.update()
        await self.day2otk.update()
        await self.day3otk.update()
        await self.day4otk.update()
        await self.day5otk.update()
        await self.day6otk.update()
        await self.day7otk.update()
        await self.day8otk.update()

    async def day_update(self, day):
        if day == 1:
            await self.day1otk.update()
        if day == 2:
            await self.day2otk.update()
        if day == 3:
            await self.day3otk.update()
        if day == 4:
            await self.day4otk.update()
        if day == 5:
            await self.day5otk.update()
        if day == 6:
            await self.day6otk.update()
        if day == 7:
            await self.day7otk.update()
        if day == 8:
            await self.day8otk.update()


def determine_point_risk(outlook: Outlook, point):
    risk = None
    for feature in outlook.data['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            risk = feature['properties']['LABEL']

    return risk

async def get_risk(session: ClientSession, day, type, point):
    outlook = Outlook(day, session, type)
    await outlook.update()

    return determine_point_risk(outlook, point)

async def get_highest_risk(session: ClientSession=None, day=1, type="cat", outlook=None):
    outlook = outlook or Outlook(day, session, type)
    await outlook.update()
    risk = None

    for feature in outlook.data['features']:
        risk = feature['properties']['LABEL']

    return risk
