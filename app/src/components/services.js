import Tooltip from "react-simple-tooltip";

function ListOfServices({ servicesInfo }) {
  return (
    <div id="PositionsList">
      {servicesInfo.map((srvInfo) => {
        return srvInfo.services.map((srv) => (
          <div
            className="service"
            style={{
              display: "flex",
              justifyContent: "space-between",
              fontSize: "12px",
              height: "40px",
              minHeight: "40px",
              maxHeight: "40px",
              padding: "5px 0px",
            }}
          >
            <Tooltip content="`{${srvInfo.hostname}:${srvInfo.port}`}">
              <div style={{ textAlign: "center", width: "9%" }}>
                <strong>{srvInfo.name}</strong>
                <span></span>
              </div>
            </Tooltip>
            <div style={{ textAlign: "center", width: "9%" }}>
              {srv.service}
            </div>
            <div style={{ textAlign: "center", width: "9%" }}>
              {srv.enabled ? "UP" : "DOWN"}
            </div>
            <button
              style={{ textAlign: "center", width: "9%" }}
              onClick={() => {}}
            >
              {srv.enabled ? "Disable" : "Enable"}
            </button>

            <div style={{ textAlign: "center", width: "70%" }}>
              {"DETAILED INFO"}
            </div>
          </div>
        ));
      })}
    </div>
  );
}

function NoServicesResults() {
  return <p>No se encontraron películas para esta búsqueda</p>;
}

export function ServicesInfo({ servicesInfo }) {
  const hasServices = servicesInfo?.length > 0;
  console.log(servicesInfo);
  return hasServices ? (
    <ListOfServices servicesInfo={servicesInfo} />
  ) : (
    <NoServicesResults />
  );
}
