import React from 'react';
import StaticMap from 'react-map-gl';
import DeckGL from '@deck.gl/react/typed';

const DeckGLMap: React.FC = () => {
  const mapboxApikey = process.env.NEXT_PUBLIC_MAPBOX_APIKEY

  return (
    <div className='w-full h-screen'>
      <DeckGL
        initialViewState={{
          latitude: 43.798,
          longitude: -79.275,
          zoom: 10,
          bearing: 0,
          pitch: 0,
        }}
        controller={true}
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
