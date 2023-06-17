import React, { useState } from 'react';

interface IQueryContextProps {
  queryData: any;
  setQueryData: (user: any) => void;
  layer: any;
  setLayer: (user: any) => void;
  lat: any;
  setLat: (user: any) => void;
  lon: any;
  setLon: (user: any) => void;
  pickedFire: any;
  setPickedFire: (user: any) => void;
  showPred: any;
  setShowPred: (user: any) => void;
  predictedFire: any;
  setPredictedFire: (user: any) => void;
}

export const QueryContext = React.createContext<IQueryContextProps>({
  queryData: {},
  setQueryData: () => { },
  layer: {},
  setLayer: () => { },
  lat: {},
  setLat: () => { },
  lon: {},
  setLon: () => { },
  pickedFire: {},
  setPickedFire: () => { },
  showPred: {},
  setShowPred: () => { },
  predictedFire: {},
  setPredictedFire: () => { },
});

export const QueryContextProvider = (props: any) => {
  const [queryData, setQueryData] = useState([]);
  const [layer, setLayer] = useState("icon")
  const [lat, setLat] = useState(0)
  const [lon, setLon] = useState(0)
  const [pickedFire, setPickedFire] = useState<any>(undefined)
  const [showPred, setShowPred] = useState(false)
  const [predictedFire, setPredictedFire] = useState<any>(undefined)

  return (
    <QueryContext.Provider
      value={{
        queryData: queryData,
        setQueryData: setQueryData,
        layer: layer,
        setLayer: setLayer,
        lat: lat,
        setLat: setLat,
        lon: lon,
        setLon: setLon,
        pickedFire: pickedFire,
        setPickedFire: setPickedFire,
        showPred: showPred,
        setShowPred: setShowPred,
        predictedFire: predictedFire,
        setPredictedFire: setPredictedFire,
      }}
    >
      {props.children}
    </QueryContext.Provider>
  );
};