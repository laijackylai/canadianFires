import React, { useState } from 'react';

interface IQueryContextProps {
  queryData: any;
  setQueryData: (user: any) => void;
  layer: any;
  setLayer: (user: any) => void;
}

export const QueryContext = React.createContext<IQueryContextProps>({
  queryData: {},
  setQueryData: () => { },
  layer: {},
  setLayer: () => { },
});

export const QueryContextProvider = (props: any) => {
  const [queryData, setQueryData] = useState([]);
  const [layer, setLayer] = useState("icon")

  return (
    <QueryContext.Provider
      value={{
        queryData: queryData,
        setQueryData: setQueryData,
        layer: layer,
        setLayer: setLayer
      }}
    >
      {props.children}
    </QueryContext.Provider>
  );
};