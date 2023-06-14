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

  const { queryData, setQueryData } = useQueryDatContext()

  const [searchInput, setSearchInput] = useState<string>("");
  const [searchMethod, setSearchMethod] = useState<string>("Absolute");
  const [showData, setShowData] = useState(false);
  const [loading, setLoading] = useState(false);

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
        setQueryData(data)
        // setShowData(true)
        setLoading(false)
      } else {
        setLoading(false)
      }
    } catch (error) {
      console.error('Error:', error);
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="z-10 absolute top-5 left-7 flex flex-row gap-5">
        {/* search bar */}
        <div className="shadow-md rounded-xl flex flex-row">
          <input
            type="text"
            placeholder='Try "Fires in ON in 05/2021" (nltk)'
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
            >
              Absolute
            </button>
            <button
              className={`p-3 text-white rounded-e-xl ${searchMethod === "Optimistic" ? "bg-gray-600" : "bg-gray-500 bg-opacity-75"}`}
              onClick={() => setSearchMethod("Optimistic")}
            >
              Optimistic
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
              <div className="overflow-auto">
                {queryData.map((d: any, i: number) => (
                  <div key={i}>
                    <div>{d.DATE}</div>
                    <div>{d.PROVINCE_CODE}</div>
                    <div>{d.LATITUDE}</div>
                    <div>{d.LONGITUDE}</div>
                    <div>{d.CAUSE}</div>
                    <div>{d.SIZE_HA}</div>
                  </div>
                ))}
              </div>
            ) : (
              <div>No data now...</div>
            )
          }
        </div>
      </div>
    </div>

  );
};

export default UI;
