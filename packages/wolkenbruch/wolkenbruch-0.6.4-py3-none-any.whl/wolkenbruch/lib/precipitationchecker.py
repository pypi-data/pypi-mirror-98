#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright (C) 2019 Christoph Fink, University of Helsinki
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 3
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.

""" Checks the precipitation over the next n hours at a given location """


import requests


__all__ = [
    "PrecipitationChecker"
]


class PrecipitationChecker:
    """ Check the forecast precipitation at a location

        Args:
            lat:        Latitude
            lon:        Longitude
            n_hours:    calculate the average precipitation
                        rate for the next `n_hours` hours
    """
    API_VERSION = "2.0"
    API_ENDPOINT = "https://api.met.no/weatherapi/locationforecast/{VERSION:s}/compact".format(VERSION=API_VERSION)
    API_HEADERS = {
        "User-agent": "python-wolkenbruch (https://gitlab.com/christoph.fink/wolkenbruch/"
    }

    def __init__(
            self,
            lat,
            lon,
            n_hours=14,
            *args,
            **kwargs
    ):
        """
        Check the forecast precipitation at a location.

        Args:
            lat:        Latitude
            lon:        Longitude
            n_hours:    calculate the average precipitation
                        rate for the next `n_hours` hours
        """
        self.lat = lat
        self.lon = lon
        self.n_hours = n_hours

        self.precipitation = []

    def _fetch_weather_forecast(self):
        forecast = requests.get(
            self.API_ENDPOINT,
            params={
                "lat": self.lat,
                "lon": self.lon
            },
            headers=self.API_HEADERS
        )
        forecast = forecast.json()

        with open("/tmp/wolkenbruch.json", "w") as f:
            import json
            f.write(json.dumps(forecast, sort_keys=True, indent=4))

        self.precipitation = [
            timestamp["data"]["next_1_hours"]["details"]["precipitation_amount"]
            for timestamp in forecast["properties"]["timeseries"]
            if "next_1_hours" in timestamp["data"]
        ]

    @property
    def hourly_precipitation_rates(self):
        """
        Retrieve precipitation rates by hour.

        How much precipitation is forecast
        for the next n hours in mm/h
        """
        if not self.precipitation:
            self._fetch_weather_forecast()
        return self.precipitation
