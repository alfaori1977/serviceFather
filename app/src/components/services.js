import Tooltip from "react-simple-tooltip";
import failImg from "../images/fail.png";
import okImg from "../images/ok.png";

function ListOfServices({ servicesInfo }) {
  return (
    <div id="PositionsList">
      {servicesInfo.map((srvGlobalInfo) => {
        return <Service srv={srvGlobalInfo} />;
      })}
    </div>
  );
}

function Service({ srv }) {
  return (
    <div
      key={srv.id}
      className="service"
      style={{
        display: "flex",
        justifyContent: "space-between",
        fontSize: "12px",
        height: "40px",
        minHeight: "20px",
        maxHeight: "20px",
        padding: "10px 20px",
      }}
    >
      <div style={{ textAlign: "center", width: "9%" }}>
        <strong>{srv.lastUpdate}</strong>
        <span></span>
      </div>
      <div style={{ textAlign: "center", width: "9%" }}>
        <strong>{srv.service}</strong>
        <span></span>
      </div>
      <div style={{ textAlign: "center", width: "9%" }}>
        {srv.rAddr}:{srv.port}
      </div>
      <div style={{ textAlign: "center", width: "9%" }}>
        {srv.enabled ? "ENABLED" : "DISABLED"}
      </div>
      <button style={{ textAlign: "center", width: "9%" }} onClick={() => {}}>
        {srv.enabled ? "Disable" : "Enable"}
      </button>
      <div style={{ textAlign: "center", width: "9%" }}>
        {srv.enabled ? "ENABLED" : "DISABLED"}
      </div>
      <div style={{ textAlign: "center", width: "9%" }}>
        {srv.returncode > 0 ? "KO" : "OK"}
      </div>
      <img
        src={srv.returncode > 0 ? failImg : okImg}
        width="22"
        alt="No se ve"
      />

      <div style={{ textAlign: "center", width: "70%" }}>
        {srv.statusMessage}
      </div>
    </div>
  );
}

function NoServicesResults() {
  return <p>No Service Father found.</p>;
}

export function ServicesInfo({ servicesInfo }) {
  const hasServices = servicesInfo?.length > 0;
  return hasServices ? (
    <ListOfServices servicesInfo={servicesInfo} />
  ) : (
    <NoServicesResults />
  );
}
