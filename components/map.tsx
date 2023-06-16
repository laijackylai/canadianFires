import React, { useEffect, useState } from 'react';
import StaticMap from 'react-map-gl';
import DeckGL from '@deck.gl/react/typed';
import { HeatmapLayer, IconLayer } from 'deck.gl/typed';
import { useQueryDatContext } from '@/contexts';

const DeckGLMap: React.FC = () => {
  const mapboxApikey = process.env.NEXT_PUBLIC_MAPBOX_APIKEY

  const { queryData, layer } = useQueryDatContext()

  useEffect(() => {
    if (queryData.length <= 0) return

    if (layer === 'heat') {
      const heatMapLayer = new HeatmapLayer({
        id: 'heatmapLayer',
        data: queryData,
        getPosition: (d) => [d.LONGITUDE, d.LATITUDE],
        getWeight: (d) => d.SIZE_HA,
        aggregation: 'SUM',
      });
      setLayers([heatMapLayer]);
    }

    if (layer === 'icon') {
      const iconLayer = new IconLayer({
        id: 'icon-layer',
        data: queryData,
        pickable: true,
        getIcon: (d) => ({
          'url': 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/icon-atlas.png',
          'width': 128,
          'height': 128,
          'anchorY': 128,
        }),
        getPosition: (d) => [d.LONGITUDE, d.LATITUDE],
        getSize: (d) => d.SIZE_HA / 100,
        sizeMinPixels: 10,
        sizeMaxPixels: 100,
        getColor: d => [Math.sqrt(d.exits), 140, 0]
      });
      setLayers([iconLayer]);
    }
  }, [queryData, layer]);

  const [layers, setLayers] = useState<any[]>([]);

  return (
    <div className='w-full h-screen'>
      <DeckGL
        initialViewState={{
          latitude: 60,
          longitude: -97,
          zoom: 3,
          bearing: 0,
          pitch: 0,
        }}
        controller={true}
        layers={layers}
      >
        <StaticMap
          mapboxAccessToken={mapboxApikey}
          mapStyle="mapbox://styles/mapbox/light-v10"
        />
      </DeckGL>
    </div>
  );
};

export default DeckGLMap;
