import Tooltip from "react-simple-tooltip";
import failImg from "../images/fail.png";
import okImg from "../images/ok.png";
import unkImg from "../images/unknown.png";

import startImg from "../images/start.png";
import stopImg from "../images/stop.png";
import restartImg from "../images/restart.png";

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
  const status = srv.statusMessage.includes("Script 'status.sh' not found")
    ? "unknown"
    : parseInt(srv.returncode);
  console.log(srv.id);
  const statusImg = status == "unknown" ? unkImg : status > 0 ? failImg : okImg;

  const perform = (action) => {
    console.log("Perform", action, srv.rAddr, srv.port, srv.service);
    const sfMgrIp = process.env.REACT_APP_SERVICE_FATHER_MGR_REPORT_IP;
    const tokenId = process.env.REACT_APP_SERVICE_FATHER_TOKEN_ID;
    const url = `http://${sfMgrIp}/perform`;

    const headers = { "Content-Type": "application/json" };
    const body = {
      ip: srv.rAddr,
      port: srv.port,
      serviceName: srv.service,
      action: action,
      token: tokenId,
    };
    console.log("Body", body);
    return fetch(url, {
      method: "POST",
      headers: headers,
      body: JSON.stringify(body),
    })
      .then((response) => response.json())
      .then((res) => console.log(res));
  };

  const start = () => {
    perform("start");
  };
  const restart = () => {
    perform("restart");
  };
  const kill = () => {
    perform("kill");
  };
  const toggleEnabled = () => {
    perform(srv.enabled ? "disable" : "enable");
  };
  // check if lastUpdate field is older than 20 seconds
  // if so, then the service is unknown
  //
  const isUnknown = () => {
    const now = new Date();
    const lastUpdate = new Date(srv.lastUpdate);
    const diff = now - lastUpdate;
    const seconds = diff / 1000;
    return seconds > 20;
  };

  const getClassName = () => {
    if (isUnknown()) return "unknown";
    if (srv?.enabled) return "service";
    return "disabled";
  };
  return (
    <div
      key={srv.id}
      className={getClassName()}
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
      <div style={{ textAlign: "center", width: "15%" }}>
        <strong>{srv.lastUpdate}</strong>
        <span></span>
      </div>
      <div style={{ textAlign: "center", width: "12%" }}>
        <strong>{srv.hostname}</strong>
      </div>
      <div style={{ textAlign: "center", width: "15%" }}>
        <strong>{srv.service}</strong>
        <span></span>
      </div>
      <div style={{ textAlign: "center", width: "10%" }}>
        {srv.rAddr}:{srv.port}
      </div>
      <div style={{ textAlign: "center", width: "9%" }}>
        {srv.enabled ? "ENABLED" : "DISABLED"}
      </div>
      <button
        style={{ textAlign: "center", width: "5%" }}
        onClick={toggleEnabled}
      >
        {srv.enabled ? "Disable" : "Enable"}
      </button>

      <img
        src={statusImg}
        style={{ padding: "2px" }}
        width="20"
        alt="No se ve"
      />
      <img
        src={startImg}
        style={{ padding: "2px" }}
        width="28"
        alt="Start"
        onClick={start}
      />
      <img
        src={restartImg}
        style={{ padding: "2px" }}
        width="28"
        alt="Restart"
        onClick={restart}
      />
      <img
        src={stopImg}
        style={{ padding: "2px" }}
        width="28"
        alt="Stop"
        onClick={kill}
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
