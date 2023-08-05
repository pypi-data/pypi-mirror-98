#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""__description__
"""

__author__ = "Christina Ludwig, GIScience Research Group, Heidelberg University"
__email__ = "christina.ludwig@uni-heidelberg.de"

import ohsome
import geojson
import geopandas as gpd


def test_parallel_user():

    # GIVEN
    bpolys = geojson.FeatureCollection([{"type": "Feature",
                                         "properties": {"id": 0},
                                         "geometry": {"coordinates": [
                                             [[[13, 51], [13, 51.1], [13.1, 51.1], [13.1, 51], [13, 51]]],
                                             [[[14, 51], [14, 51.1], [14.1, 51.1], [14.1, 51], [14, 51]]]],
                                                      "type": "MultiPolygon"}},
                                        {"type": "Feature",
                                         "properties": {"id": 1},
                                         "geometry": {"coordinates": [
                                             [[[13, 51], [13, 51.1], [13.1, 51.1], [13.1, 51], [13, 51]]],
                                             [[[14, 51], [14, 51.1], [14.1, 51.1], [14.1, 51], [14, 51]]]],
                                             "type": "MultiPolygon"}}
                                        ])

    bpolys_df = gpd.GeoDataFrame().from_features(bpolys)
    timeperiod = "2017-01-01,2018-01-01"
    keys = ["amenity"]
    values = [""]
    format = "json"
    properties = ["metadata"]

    # WHEN
    client = ohsome.OhsomeClientParallel(chunksize=1)
    response = client.users.count.groupBy.boundary.post(bpolys=bpolys_df, time=timeperiod, keys=keys, values=values,
                                                           format=format, properties=properties)
    result = response.as_dataframe()
    del client

    # THEN
    assert result["value"][0] == 33.
