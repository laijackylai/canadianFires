import React, { useEffect, useState } from 'react';
import StaticMap from 'react-map-gl';
import DeckGL from '@deck.gl/react/typed';
import { HeatmapLayer } from 'deck.gl/typed';
import { useQueryDatContext } from '@/contexts';

const DeckGLMap: React.FC = () => {
  const mapboxApikey = process.env.NEXT_PUBLIC_MAPBOX_APIKEY

  const { queryData } = useQueryDatContext()

  useEffect(() => {
    if (queryData.length <= 0) return
    const heatMapLayer = new HeatmapLayer({
      id: 'heatmapLayer',
      data: queryData,
      getPosition: (d) => [d.LONGITUDE, d.LATITUDE],
      getWeight: (d) => d.SIZE_HA,
      aggregation: 'SUM',
    });
    setLayers([heatMapLayer]);
  }, [queryData]);

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
