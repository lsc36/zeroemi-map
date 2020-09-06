import logging

import googlemaps
import simplekml

import config
import crawler


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def main():
    shops = crawler.shop_list()
    log.info('found %s shops', len(shops))

    gmaps = googlemaps.Client(key=config.GOOGLEMAPS_API_KEY)
    kml = simplekml.Kml()

    for shop in shops:
        gc = gmaps.geocode(shop['address'])
        if len(gc) == 0:
            log.error('shop %s has no matching locations', shop['name'])
            continue
        if len(gc) != 1:
            log.warn('shop %s has %s matching locations', shop['name'], len(gc))
        loc = gc[0]['geometry']['location']
        kml.newpoint(name=shop['name'], coords=[(loc['lng'], loc['lat'])])

    out = 'zeroemi_map.kml'
    log.info('writing output to %s', out)
    kml.save(out)


if __name__ == '__main__':
    main()
