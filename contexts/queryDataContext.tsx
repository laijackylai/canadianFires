import React, { useState } from 'react';

interface IQueryContextProps {
  queryData: any;
  setQueryData: (user: any) => void;
}

export const QueryContext = React.createContext<IQueryContextProps>({
  queryData: {},
  setQueryData: () => { },
});

export const QueryContextProvider = (props: any) => {
  const [queryData, setQueryData] = useState([]);

  return (
    <QueryContext.Provider
      value={{
        queryData: queryData,
        setQueryData: setQueryData,
      }}
    >
      {props.children}
    </QueryContext.Provider>
  );
};