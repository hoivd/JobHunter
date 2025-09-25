export class WSClient {
  constructor(url) {
    this.ws = new WebSocket(url);
    this.callbacks = [];

    this.ws.onopen = () => console.log("✅ WebSocket connected");

    this.ws.onmessage = (event) => {
      this.callbacks.forEach((cb) => cb(event.data));
    };

    this.ws.onclose = () => console.log("❌ WebSocket closed");

    this.ws.onerror = (err) => console.error("WebSocket error:", err);
  }

  send(message) {
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(message);
    } else {
      console.warn("WebSocket not open");
    }
  }

  onMessage(callback) {
    this.callbacks.push(callback);
  }

  close() {
    this.ws.close();
  }
}
