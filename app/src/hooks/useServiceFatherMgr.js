import { useState, useMemo, useEffect } from "react";
import useSWR from "swr";

import response from "../mooks/search.json";

export default function useServiceFatherMgr() {
  const [services, setServices] = useState([]);

  const fetchStatus = (...args) => {
    const [id] = args;
    const url = "http://localhost:15000/status";
    return fetch(url)
      .then((response) => response.json())
      .then((res) => setServices(res.result))
      .catch((error) => setServices([]));
  };

  const { data, error } = useSWR([`fetchStatus`], fetchStatus, {
    refreshInterval: 3000,
  });

  /*const sortedServices = [...services].sort((b, a) =>
    a.name.localeCompare(b.name)
  );*/

  return { servicesInfo: services };
}
