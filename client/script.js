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
  events.forEach((evType) =>
    document.getElementById(id).addEventListener(evType, (ev) => {
      const touch = ev.targetTouches[0];
      server.send(
        `${id} ${evType} ${Math.trunc(touch.screenX)} ${Math.trunc(touch.screenY)
        }`,
      );
    })
  );
}

function broadcastEvents(id, events, overrideId) {
  events.forEach((evType) =>
    document.getElementById(id).addEventListener(evType, () => {
      server.send(`${overrideId || id} ${evType}`);
    })
  );
}

broadcastScrollEvents("touchpad", ["touchstart", "touchmove"]);
broadcastScrollEvents("mousewheel", ["touchstart", "touchmove"]);

broadcastEvents("touchpad", ["mousedown", "mouseup"], "lmb");
broadcastEvents("lmb", ["touchstart", "touchend"]);
broadcastEvents("rmb", ["touchstart", "touchend"]);
