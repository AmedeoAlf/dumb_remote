document.getElementById("fs-button").addEventListener(
  "click",
  () => document.getElementById("main-card").requestFullscreen(),
);

let server;

function buildServer() {
  server = new WebSocket("/ws");

  server.addEventListener("open", () => {
    setConnectionIndicator("green", "Connected");
  });

  server.addEventListener("close", (ev) => {
    setConnectionIndicator("red", `Disconnected (${ev.code}) - reconnecting`);
    const tryConnection = () => {
      switch (server.readyState) {
        case WebSocket.OPEN:
          break;
        case WebSocket.CLOSING:
        case WebSocket.CLOSED:
          buildServer();
        case WebSocket.OPENING:
          setTimeout(tryConnection(), 100);
      }
    };
    tryConnection();
  });
}

buildServer();

function setConnectionIndicator(color, description) {
  const indicator = document.getElementById("connection-indicator");
  indicator.querySelector(".state-color").style.backgroundColor = color;
  indicator.querySelector(".state-label").innerHTML = description;
}

function broadcastScrollEvents(id, events) {
  console.log(id, events);
  events.forEach((evType) =>
    document.getElementById(id).addEventListener(evType, (ev) => {
      const touch = ev.targetTouches[0];
      server.send(
        `${id} ${evType} ${touch.screenX.toFixed(2)} ${touch.screenY.toFixed(2)
        }`,
      );
    })
  );
}

function broadcastEvents(id, events, overrideId) {
  console.log(id, events, overrideId);
  events.forEach((evType) =>
    document.getElementById(id).addEventListener(evType, () => {
      server.send(`${overrideId || id} ${evType}`);
    })
  );
}

/*EVENTLIST*/
