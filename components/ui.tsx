import { useQueryDatContext } from "@/contexts";
import axios, { AxiosResponse } from "axios";
import { NextPage } from "next";
import { useEffect, useState } from "react";

type Props = {

}

const UI: NextPage<Props> = () => {
  useEffect(() => {
    document.body.style.overflow = "hidden"
  }, [])

  const { queryData, setQueryData, layer, setLayer, lat, setLat, lon, setLon, setPickedFire, showPred, setShowPred, setPredictedFire } = useQueryDatContext()

  const [searchInput, setSearchInput] = useState<string>("");
  const [searchMethod, setSearchMethod] = useState<string>("Absolute");
  const [showData, setShowData] = useState(false);
  const [loading, setLoading] = useState(false);
  const [predicting, setPredicting] = useState(false);

  const [predYear, setPredYear] = useState(new Date().getFullYear().toString())
  const [predMonth, setPredMonth] = useState((new Date().getMonth() + 1).toString())
  const [predDay, setPredDay] = useState(new Date().getDate().toString())
  const [predMeanTemp, setPredMeanTemp] = useState("")
  const [predMeanRain, setPredMeanRain] = useState("")
  const [predMeanSnow, setPredMeanSnow] = useState("")
  const [ecoZone, setEcoZone] = useState('0')

  const handleToggleData = () => {
    setShowData(!showData);
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchInput(event.target.value);
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      search();
    }
  };

  const search = async () => {
    setLoading(true)
    setQueryData([])
    const queryParams = new URLSearchParams(
      [
        ["strategy", '"' + searchMethod + '"'],
        ["query", '"' + searchInput + '"']
      ]
    );
    try {
      const response: AxiosResponse = await axios.get(`/api/nlpSearch?${queryParams}`);
      const { result, data } = response.data
      if (result.trim() === "success") {
        console.log(data)
        setQueryData(data)
        if (data.length === 0) {
          alert('No data')
        }
        // setShowData(true)
        setLoading(false)
      } else {
        alert('No data')
        setLoading(false)
      }
    } catch (error) {
      alert('Error: check console')
      console.error('Error:', error);
      setLoading(false)
    }
  }

  const predict = async () => {
    setPredicting(true)
    const queryParams = new URLSearchParams(
      [
        ["lat", lat],
        ["lon", lon],
        ["year", predYear],
        ["month", predMonth],
        ["day", predDay],
        ["meanTemp", predMeanTemp],
        ["meanRain", predMeanRain],
        ["meanSnow", predMeanSnow],
        ["ecoZone", ecoZone]
      ]
    );
    try {
      const response: AxiosResponse = await axios.get(`/api/pred?${queryParams}`);
      const { result, data } = response.data
      if (result.trim() === "success") {
        setPredictedFire(data[0])
        setPredicting(false)
      } else {
        setPredicting(false)
      }
    } catch (error) {
      console.error('Error:', error);
      setPredicting(false)
    }
  }

  return (
    <div>
      <div className="z-10 absolute top-5 left-7 flex flex-row gap-5">
        {/* search bar */}
        <div className="shadow-md rounded-xl flex flex-row">
          <input
            type="text"
            placeholder='Search fires in Ontario from 1930-2021'
            className="p-3 rounded-s-xl text-black w-80"
            value={searchInput}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
          />
          <button
            className="p-3 text-white bg-gray-500 bg-opacity-75 rounded-e-xl"
            onClick={search}
            disabled={loading}
          >
            {loading ?
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
              </svg>
              :
              <div>Search</div>
            }
          </button>
        </div>
        {/* query type */}
        <div className='flex flex-row'>
          <div className="rounded-xl shadow-md">
            <button
              className={`p-3 text-white rounded-s-xl ${searchMethod === "Absolute" ? "bg-gray-600" : "bg-gray-500 bg-opacity-75"}`}
              onClick={() => setSearchMethod("Absolute")}
              disabled={loading}
            >
              Absolute
            </button>
            <button
              className={`p-3 text-white rounded-e-xl ${searchMethod === "Optimistic" ? "bg-gray-600" : "bg-gray-500 bg-opacity-75"}`}
              onClick={() => setSearchMethod("Optimistic")}
              disabled={loading}
            >
              Optimistic
            </button>
          </div>
        </div>
        {/* layer */}
        <div className='flex flex-row'>
          <div className="rounded-xl shadow-md items-center">
            <button
              className={`p-3 text-white rounded-s-xl ${layer === "icon" ? "bg-gray-600" : "bg-gray-500 bg-opacity-75"}`}
              onClick={() => setLayer("icon")}
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
              </svg>
            </button>
            <button
              className={`p-3 text-white rounded-e-xl ${layer === "heat" ? "bg-gray-600" : "bg-gray-500 bg-opacity-75"}`}
              onClick={() => setLayer("heat")}
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M15.362 5.214A8.252 8.252 0 0112 21 8.25 8.25 0 016.038 7.048 8.287 8.287 0 009 9.6a8.983 8.983 0 013.361-6.867 8.21 8.21 0 003 2.48z" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 18a3.75 3.75 0 00.495-7.467 5.99 5.99 0 00-1.925 3.546 5.974 5.974 0 01-2.133-1A3.75 3.75 0 0012 18z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      {/* data */}
      <div className="z-10 absolute top-5 right-7 flex flex-row rounded-xl shadow-md ">
        <button
          className="flex flex-row gap-1 bg-gray-500 p-3 rounded-xl bg-opacity-75 items-center"
          onClick={handleToggleData}
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 text-white">
            <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 12h-15m0 0l6.75 6.75M4.5 12l6.75-6.75" />
          </svg>
          <div className="text-white">Data</div>
        </button>
      </div>
      <div className={`text-black overflow-hidden z-20 absolute top-0 -right-0 h-screen bg-white p-7 transition-transform duration-500 ease-in-out ${showData ? 'translate-x-0' : 'translate-x-full'}`}>
        <div className="flex flex-col gap-5">
          <button onClick={handleToggleData}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          {
            queryData && queryData.length > 0 ? (
              <div className="overflow-auto" style={{ maxHeight: '87.5vh' }}>
                <div>
                  <div className="mb-3">Total no. of rows: {queryData.length}</div>
                  <table className="table-auto border-collapse border">
                    <thead className="sticky top-0 bg-gray-200">
                      <tr>
                        <th className="border px-4 py-2">Date</th>
                        <th className="border px-4 py-2">Province Code</th>
                        <th className="border px-4 py-2">Latitude</th>
                        <th className="border px-4 py-2">Longitude</th>
                        <th className="border px-4 py-2">Cause</th>
                        <th className="border px-4 py-2">Size (HA)</th>
                      </tr>
                    </thead>
                    <tbody>
                      {queryData.map((d: any, i: number) => (
                        <tr key={i}>
                          <td className="border px-4 py-2">{d.DATE}</td>
                          <td className="border px-4 py-2">{d.PROVINCE_CODE}</td>
                          <td className="border px-4 py-2">{d.LATITUDE}</td>
                          <td className="border px-4 py-2">{d.LONGITUDE}</td>
                          <td className="border px-4 py-2">{d.CAUSE}</td>
                          <td className="border px-4 py-2">{d.SIZE_HA}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ) : (
              <div>No data now...</div>
            )
          }
        </div>
      </div>
      {!showPred &&
        <button
          className="text-white z-10 absolute top-20 left-7 flex flex-row gap-3 p-3 bg-gray-500 opacity-75 rounded-xl shadow-md items-center"
          onClick={() => {
            setShowPred(true)
            setPickedFire(undefined)
          }}
        >
          <div>Predict Fires in ON</div>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-5 h-5">
            <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
          </svg>
        </button>
      }
      <div className={`text-white z-10 absolute top-20 left-7 flex flex-col gap-3 p-5 bg-gray-500 opacity-75 rounded-xl shadow-md transform transition-transform duration-500 ${showPred ? 'translate-x-0' : ' -translate-x-96'}`}>
        <div className="flex flex-row gap-2">
          <button onClick={() => setShowPred(false)}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 text-white">
              <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 12h-15m0 0l6.75 6.75M4.5 12l6.75-6.75" />
            </svg>
          </button>
          <div>Predict fires in Ontario</div>
        </div>
        <div className="flex flex-row gap-2 items-center justify-between">
          <div>Lat: </div>
          <input
            type="text"
            placeholder='Latitude'
            className="p-3 rounded-xl text-black w-50"
            value={lat}
            onChange={e => setLat(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter') { predict() } }}
          />
        </div>
        <div className="flex flex-row gap-2 items-center justify-between">
          <div>Lon: </div>
          <input
            type="text"
            placeholder='Longitude'
            className="p-3 rounded-xl text-black w-50"
            value={lon}
            onChange={e => setLon(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter') { predict() } }}
          />
        </div>
        <div className="flex flex-row gap-2 items-center justify-between">
          <div>Year: </div>
          <input
            type="text"
            placeholder='Year'
            className="p-3 rounded-xl text-black w-50"
            value={predYear}
            onChange={e => setPredYear(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter') { predict() } }}
          />
        </div>
        <div className="flex flex-row gap-2 items-center justify-between">
          <div>Month: </div>
          <input
            type="text"
            placeholder='Month'
            className="p-3 rounded-xl text-black w-50"
            value={predMonth}
            onChange={e => setPredMonth(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter') { predict() } }}
          />
        </div>
        <div className="flex flex-row gap-2 items-center justify-between">
          <div>Day: </div>
          <input
            type="text"
            placeholder='Day'
            className="p-3 rounded-xl text-black w-50"
            value={predDay}
            onChange={e => setPredDay(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter') { predict() } }}
          />
        </div>
        <div className="flex flex-row gap-2 items-center justify-between">
          <div>Mean Temp: </div>
          <input
            type="text"
            placeholder='Mean Temperature'
            className="p-3 rounded-xl text-black w-50"
            value={predMeanTemp}
            onChange={e => setPredMeanTemp(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter') { predict() } }}
          />
        </div>
        <div className="flex flex-row gap-2 items-center justify-between">
          <div>Mean Pre: </div>
          <input
            type="text"
            placeholder='Mean Precipitation'
            className="p-3 rounded-xl text-black w-50"
            value={predMeanRain}
            onChange={e => setPredMeanRain(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter') { predict() } }}
          />
        </div>
        <div className="flex flex-row gap-2 items-center justify-between">
          <div>Mean Snow: </div>
          <input
            type="text"
            placeholder='Mean Snowfall'
            className="p-3 rounded-xl text-black w-50"
            value={predMeanSnow}
            onChange={e => setPredMeanSnow(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter') { predict() } }}
          />
        </div>
        <div className="relative flex flex-row items-center gap-3 justify-between">
          <div>Eco Zone: </div>
          <select
            className="block appearance-none bg-white text-black py-2 px-4 pr-8 rounded-xl leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            value={ecoZone || ''}
            onChange={(e) => { setEcoZone(e.target.value) }}
          >
            {[0, 6, 8, 15].map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>
        <button
          className="p-3 text-white bg-gray-400 bg-opacity-75 rounded-xl w-fit"
          onClick={predict}
          disabled={predicting}
        >
          {predicting ?
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
              <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
            </svg>
            :
            <div>Predict</div>
          }
        </button>
      </div>
    </div>

  );
};

export default UI;
