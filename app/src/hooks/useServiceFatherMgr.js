import { useState } from "react";
import useSWR from "swr";

import response from "../mooks/search.json";

export default function useServiceFatherMgr() {
  const [services, setServices] = useState([]);

  const fetchStatus = (...args) => {
    const [id] = args;
    const url = "http://localhost:15000/status";
    return fetch(url)
      .then((response) => response.json())
      .then((res) => setServices(res.result));
  };

  const { data, error } = useSWR([`fetchStatus`], fetchStatus);

  return { servicesInfo: services };
}
