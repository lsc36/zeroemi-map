import logging

import googlemaps
import simplekml

import config
import crawler


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main():
    shops = crawler.shop_list()

    gmaps = googlemaps.Client(key=config.GOOGLEMAPS_API_KEY)
    kml = simplekml.Kml()

    for shop in shops:
        gc = gmaps.geocode(shop['address'])
        if len(gc) == 0:
            log.error('shop %s (%s) has no matching locations',
                      shop['name'], shop['address'])
            continue
        if len(gc) != 1:
            log.warning('shop %s (%s) has %s matching locations',
                        shop['name'], shop('address'), len(gc))
        loc = gc[0]['geometry']['location']
        kml.newpoint(name=shop['name'],
                     description=shop['address'],
                     coords=[(loc['lng'], loc['lat'])])

    out = 'zeroemi_map.kml'
    log.info('writing output to %s', out)
    kml.save(out)


if __name__ == '__main__':
    main()
