import { useContext } from 'react';

import { QueryContext } from './queryDataContext';

export const useQueryDatContext = () => useContext(QueryContext)