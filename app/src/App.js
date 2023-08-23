import "./App.css";
import useServiceFatherMgr from "./hooks/useServiceFatherMgr";
import { ServicesInfo } from "./components/services";

import response from "./mooks/search.json";

function App() {
  const { servicesInfo } = useServiceFatherMgr();

  return (
    <div className="page">
      <header>
        <h1>Service Father Manager</h1>
      </header>

      <main>
        <ServicesInfo servicesInfo={servicesInfo} />
      </main>
    </div>
  );
}

export default App;
