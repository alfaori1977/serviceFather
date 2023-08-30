import "./App.css";
import useServiceFatherMgr from "./hooks/useServiceFatherMgr";
import { ServicesInfo } from "./components/services";
import LabeledCheckbox from "./components/labeledCheckbox";

import { useState } from "react";

import response from "./mooks/search.json";

function App() {
  const [sort, setSort] = useState(false);
  const [sortByHost, setSortByHost] = useState(false);

  const [hideDisabled, setHideDisabled] = useState(true);

  const { servicesInfo } = useServiceFatherMgr({
    sort,
    hideDisabled,
    sortByHost,
  });

  const handleSortByHost = () => {
    setSortByHost(!sortByHost);
  };

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
        <LabeledCheckbox
          label="Sort by Hostname"
          value={sortByHost}
          setValue={handleSortByHost}
          id="sortByHostChk"
        />
        <LabeledCheckbox
          label="Hide Disabled"
          value={hideDisabled}
          setValue={handleHideDisabled}
          id="hideDisabledChk"
        />
        <ServicesInfo servicesInfo={servicesInfo} />
      </main>
    </div>
  );
}

export default App;
