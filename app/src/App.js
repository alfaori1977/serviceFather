import logo from "./logo.svg";
import "./App.css";
import useServiceFatherMgr from "./hooks/useServiceFatherMgr";
import { ServicesInfo } from "./components/services";

function App() {
  const { servicesInfo } = useServiceFatherMgr();
  console.log(servicesInfo);

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
