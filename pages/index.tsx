import UI from '@/components/ui';
import { QueryContextProvider } from '@/contexts/queryDataContext';
import dynamic from 'next/dynamic';
import { NextPage } from 'next/types';
const Map = dynamic(() => import('@/components/map'), { ssr: false });

type Props = {

}

const App: NextPage<Props> = ({ }) => {
  return (
    <QueryContextProvider>
      <UI />
      <Map />
    </QueryContextProvider>
  );
}

export default App