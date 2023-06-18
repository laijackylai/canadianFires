import React, { useEffect, useState } from 'react';
import StaticMap from 'react-map-gl';
import DeckGL from '@deck.gl/react/typed';
import { HeatmapLayer, IconLayer } from 'deck.gl/typed';
import { useQueryDatContext } from '@/contexts';
import Tooltip from './tooltip';
import { fireIcon, predFireIcon } from './icons';

const DeckGLMap: React.FC = () => {
  const mapboxApikey = process.env.NEXT_PUBLIC_MAPBOX_APIKEY

  const { queryData, layer, setLat, setLon, pickedFire, setPickedFire, setShowPred, predictedFire } = useQueryDatContext()

  useEffect(() => {
    if (layer === 'heat') {
      const heatMapLayer = new HeatmapLayer({
        id: 'heatmapLayer',
        data: queryData,
        getPosition: (d) => [d.LONGITUDE, d.LATITUDE],
        getWeight: (d) => d.SIZE_HA,
        aggregation: 'SUM',
      });
      setLayers(l => [heatMapLayer]);
    }

    if (layer === 'icon') {
      const iconLayer = new IconLayer({
        id: 'icon-layer',
        data: queryData,
        pickable: true,
        getIcon: () => 'marker', // Return the icon ID
        iconAtlas: fireIcon(),
        iconMapping: {
          marker: {
            x: 0,
            y: 0,
            width: 512,
            height: 512,
            anchorY: 512,
          },
        },
        getPosition: (d) => [d.LONGITUDE, d.LATITUDE],
        getSize: (d) => d.SIZE_HA / 500,
        sizeMinPixels: 20,
        sizeMaxPixels: 75,
        sizeScale: 500,
        onClick: (pickingInfo, event) => {
          setShowPred(false)
          if (pickingInfo && pickingInfo.object) {
            setPickedFire(pickingInfo.object)
          } else {
            setPickedFire(undefined)
          }
        },
      });
      setLayers(l => [iconLayer]);
    }
  }, [queryData, layer]);

  useEffect(() => {
    console.log(predictedFire)
    if (predictedFire && predictedFire['SIZE_HA'] > 0) {
      const predictedFireLayer = new IconLayer({
        id: `pred-layer-${Math.random()}`,
        data: [predictedFire],
        pickable: true,
        getIcon: () => 'marker', // Return the icon ID
        iconAtlas: predFireIcon(),
        iconMapping: {
          marker: {
            x: 0,
            y: 0,
            width: 612,
            height: 612,
            anchorY: 612,
          },
        },
        getPosition: (d) => [d.LONGITUDE, d.LATITUDE],
        getSize: (d) => d.SIZE_HA / 500,
        sizeMinPixels: 20,
        sizeMaxPixels: 75,
        sizeScale: 500,
        onClick: (pickingInfo, event) => {
          setShowPred(false)
          if (pickingInfo && pickingInfo.object) {
            setPickedFire(pickingInfo.object)
          } else {
            setPickedFire(undefined)
          }
        },
      });
      setLayers(l => [...l, predictedFireLayer])
    }
    if (predictedFire && predictedFire['SIZE_HA'] < 0) {
      alert('No fire')
    }
  }, [predictedFire])


  const [layers, setLayers] = useState<any[]>([]);

  const handleMapClick = (event: any) => {
    const lon = event.coordinate[0]
    const lat = event.coordinate[1]
    setLat(lat)
    setLon(lon)
  }

  return (
    <div className='w-full h-screen'>
      <DeckGL
        initialViewState={{
          latitude: 50.42842205069528,
          longitude: -83.93777509786482,
          zoom: 4.25,
          bearing: 0,
          pitch: 0,
        }}
        controller={true}
        layers={layers}
        onClick={handleMapClick}
      >
        <StaticMap
          mapboxAccessToken={mapboxApikey}
          mapStyle="mapbox://styles/mapbox/light-v10"
        />
      </DeckGL>
      {pickedFire && <Tooltip data={pickedFire} setPickedFire={setPickedFire} />}
    </div>
  );
};

export default DeckGLMap;
