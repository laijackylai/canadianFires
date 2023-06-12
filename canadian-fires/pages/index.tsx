import UI from '@/components/ui';
import dynamic from 'next/dynamic';
const Map = dynamic(() => import('@/components/map'), { ssr: false });

const App = () => {
  return (
    <>
      <UI />
      <Map />
    </>
  );
}

export default App