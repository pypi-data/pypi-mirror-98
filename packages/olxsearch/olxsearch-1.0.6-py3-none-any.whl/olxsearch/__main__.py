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

""" Search small ad listings on OLX Indonesia
    and save them in a local PostGIS/PostgreSQL database """


import argparse
import os
import os.path

import geoalchemy2
import requests
import sqlalchemy.ext.declarative
import sqlalchemy.orm

from .olxsearch import OlxSearch


class Base:
    @sqlalchemy.orm.declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = sqlalchemy.ext.declarative.declarative_base(cls=Base)


class AbstractOlxRecord(Base):
    __abstract__ = True

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)

    title = sqlalchemy.Column(sqlalchemy.Text)
    description = sqlalchemy.Column(sqlalchemy.Text)

    created_at = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True))
    created_at_first = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True))
    republish_date = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True))

    price = sqlalchemy.Column(sqlalchemy.Integer)
    price_currency = sqlalchemy.Column(sqlalchemy.Text)

    images = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.Text))

    geom = sqlalchemy.Column(geoalchemy2.Geometry("POINT", 4326))

    @classmethod
    def from_data_dict(cls, data):
        """Create a new OlxRecord from a data dict as returned by OlxSearch."""
        # create a geometry out of lat/lon coordinates
        try:
            longitude = float(data["lon"])
            latitude = float(data["lat"])
            assert longitude != 0 and latitude != 0
            data["geom"] = "SRID=4326;POINT({longitude:f} {latitude:f})".format(
                longitude=longitude,
                latitude=latitude
            )
        except (
            AssertionError,  # lon/lat is at exactly 0°N/S, 0°W/E -> bogus
            KeyError,        # not contained in API dict
            TypeError        # weird data returned
        ):
            pass
        finally:
            del data["lon"]
            del data["lat"]

        # unpack the price information
        data["price"], data["price_currency"] = data["price"]

        return cls(**data)


def _download_listing_images(listing, media_directory):
    """ Download all images attached to an OLX listing """
    destination_directory = os.path.join(
        media_directory,
        listing["id"]
    )
    os.makedirs(
        destination_directory,
        exist_ok=True
    )
    for url in listing["images"]:
        filename = os.path.join(
            destination_directory,
            "{:s}.jpg".format(
                url.split('/')[-2]
            )
        )
        _download_file(url, filename)


def _download_file(url, filename):
    with requests.get(
            url,
            stream=True
    ) as r:
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=None):
                f.write(chunk)


def main():
    """ Search small ad listings on OLX Indonesia
        and save them in a local PostGIS/PostgreSQL database """
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-c",
        "--country",
        help="""Query the OLX market place for COUNTRY.
                Specify more than one country using multiple switches
                (-c COUNTRY1 -c COUNTRY2) """,
        choices=(
            "Argentina",
            "Bulgaria",
            "Bosnia",
            "Brazil",
            "Colombia",
            "Costa Rica",
            "Ecuador",
            "Egypt",
            "Guatemala",
            "India",
            "Indonesia",
            "Kazakhstan",
            "Lebanon",
            "Oman",
            "Pakistan",
            "Panama",
            "Peru",
            "Poland",
            "Portugal",
            "Romania",
            "San Salvador",
            "South Africa",
            "Ukraine",
            "Uzbekistan"
        ),
        action="append",
        required=True
    )
    argparser.add_argument(
        "search_terms",
        help="""Query the titles and descriptions of the listings
                on the OLX market place for this""",
        nargs="+"
    )
    argparser.add_argument(
        "-d",
        "--connection-string",
        help="""Store the retrieved data in this GeoAlchemy2 compatible data base
                (default: "postgresql:///olx") """,
        default="postgresql:///olx"
    )
    argparser.add_argument(
        "-t",
        "--table",
        help="""Store the data in a table with this name
                (default: same as the first search_term)""",
        default=None
    )
    argparser.add_argument(
        "-m",
        "--media-directory",
        help="""Download images to this directory""",
        default="./media"
    )
    args = argparser.parse_args()

    if args.table is None:
        args.table = args.search_terms[0]

    OlxRecord = type(args.table, (AbstractOlxRecord,), {})

    engine = sqlalchemy.create_engine(args.connection_string)
    Base.metadata.create_all(engine)

    for search_term in args.search_terms:
        for country in args.country:
            for listing in OlxSearch(country, search_term).listings:
                with sqlalchemy.orm.Session(engine) as session, session.begin():
                    olx_record = OlxRecord.from_data_dict(listing)
                    session.merge(olx_record)
                    del olx_record


if __name__ == "__main__":
    main()
