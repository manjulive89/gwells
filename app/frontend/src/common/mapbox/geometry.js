import mapboxgl from 'mapbox-gl'
import { pick } from 'lodash'

export const CENTRE_LNG_LAT_BC = new mapboxgl.LngLat(-126.495, 54.459)
export const DEFAULT_MAP_ZOOM = 4
export const BC_LAT_LNG_BOUNDS = new mapboxgl.LngLatBounds(new mapboxgl.LngLat(-114.0541379, 60.0023), new mapboxgl.LngLat(-139.0536706, 48.2245556))

// Builds a MapBox LngLat from the feature's geometry
export function getLngLatOfPointFeature (feature) {
  return new mapboxgl.LngLat(...feature.geometry.coordinates)
}

// Extends the bounds based on an array of lng / lat points
export function computeBoundsFromCoords (coords) {
  return coords.reduce((bounds, coord) => {
    return bounds.extend(coord)
  }, new mapboxgl.LngLatBounds(coords[0], coords[0]))
}

// Computes the bounds of a MultiPolygon geometry
export function computeBoundsFromMultiPolygon (coordinates) {
  const bounds = new mapboxgl.LngLatBounds()

  // Loop through MultiPolygon → Polygon → Line array to compute bounds
  coordinates.forEach((polygonCoords) => {
    polygonCoords.forEach((coords) => {
      bounds.extend(computeBoundsFromCoords(coords))
    })
  })

  return bounds
}

export function containsBounds (containerBounds, testBounds) {
  if (!containerBounds.contains(testBounds.getSouthWest())) {
    return false
  } else if (!containerBounds.contains(testBounds.getNorthEast())) {
    return false
  } else if (!containerBounds.contains(testBounds.getNorthWest())) {
    return false
  } else if (!containerBounds.contains(testBounds.getSouthEast())) {
    return false
  }

  return true
}

export function buildWellsGeoJSON (wells = [], properties = []) {
  const features = wells.map((well) => {
    return {
      type: 'Feature',
      properties: properties.length > 0 ? pick(properties) : properties,
      geometry: {
        type: 'Point',
        coordinates: [well.longitude, well.latitude]
      }
    }
  })

  return {
    type: 'FeatureCollection',
    features
  }
}

export function convertLngLatBoundsToDirectionBounds (lngLatBounds) {
  const sw = lngLatBounds.getSouthWest()
  const ne = lngLatBounds.getNorthEast()

  return {
    sw_lat: sw.lat,
    sw_long: sw.lng,
    ne_lat: ne.lat,
    ne_long: ne.lng
  }
}

export function boundsCompletelyContains (boundsOuter, boundsInner) {
  const boundsPoints = [
    boundsInner.getSouthWest(),
    boundsInner.getSouthEast(),
    boundsInner.getNorthEast(),
    boundsInner.getNorthWest()
  ]

  return boundsPoints.every((coordinate) => {
    return boundsOuter.contains(coordinate)
  })
}
