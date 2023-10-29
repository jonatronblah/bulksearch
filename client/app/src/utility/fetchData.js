import useSWR from "swr";



const fetcher = (...args) => fetch(...args).then(res => res.json());

/*
export default function useMatters () {
  const { data, error, mutate } = useSWR(`/watchlist/api/matters`, fetcher
);

return {
  data: data,
  isLoading: !error && !data,
  isError: error,
  mutate: mutate
};
}
  */


function useData (path) {
    
    const { data, error } = useSWR(`/watchlist/api/${path}`, fetcher, 

    );
  
    return {
      data: data,
      isLoading: !error && !data,
      isError: error
    };
  }


export default useData;
