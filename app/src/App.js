import "./App.css";
import useServiceFatherMgr from "./hooks/useServiceFatherMgr";
import { ServicesInfo } from "./components/services";

import { useState } from "react";

import response from "./mooks/search.json";

function App() {
  const [sort, setSort] = useState(false);
  const [hideDisabled, setHideDisabled] = useState(false);

  const { servicesInfo } = useServiceFatherMgr({ sort, hideDisabled });

  const handleSort = () => {
    setSort(!sort);
  };

  const handleHideDisabled = () => {
    setHideDisabled(!hideDisabled);
  };

  return (
    <div className="page">
      <header>
        <h1>Service Father Manager</h1>
      </header>

      <main>
        <div>
          <input
            onChange={handleSort}
            id={"sortCheckbox"}
            type="checkbox"
            checked={sort}
          />
          <label htmlFor={"sortCheckbox"}>Sort</label>
        </div>
        <div>
          <input
            onChange={handleHideDisabled}
            id={"handleHideDisabled"}
            type="checkbox"
            checked={hideDisabled}
          />
          <label htmlFor={"handleHideDisabled"}>
            {hideDisabled ? "Show Disabled" : "Hide Disabled"}
          </label>
        </div>
        <ServicesInfo servicesInfo={servicesInfo} />
      </main>
    </div>
  );
}

export default App;
