type Props = {
  data: any,
  setPickedFire: any
}

const Tooltip: React.FC<Props> = ({ data, setPickedFire }) => {
  return (
    <div className="absolute z-10 bottom-5 left-5 p-4 bg-gray-500 text-white opacity-75 rounded-lg flex flex-col">
      <button onClick={() => setPickedFire(undefined)} className="pb-2">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
      <div>Selected fire</div>
      <div>Fire Date: {data['DAY']}/{data['MONTH']}/{data['YEAR']}</div>
      <div>Latitude: {data['LATITUDE']}</div>
      <div>Longitude: {data['LONGITUDE']}</div>
      <div>Cause: {causeMap(data['CAUSE'])}</div>
      <div>Size in HA: {data['SIZE_HA']}</div>
      <div>Out date: {data['OUT_DATE'] === null ? "Unknown" : data['OUT_DATE']}</div>
    </div>
  )
}

const causeMap = (c: string) => {
  switch (c) {
    case 'u':
      return 'Unknow Cause'
    case 'l':
      return 'Lighting'
    case 'h':
      return 'Human'
    case 'h-pb':
      return 'Prescribed burn (human caused)'
    case 're':
      return 'Reburn'
    default:
      break;
  }
}


export default Tooltip