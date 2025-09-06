const http = require('http');
const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');

const PORT = 8080;

const server = http.createServer((req, res) => {
  if (req.url === '/') {
    const html = fs.readFileSync(path.join(__dirname, 'index.html'));
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(html);
  }
});

const wss = new WebSocket.Server({ server });

wss.on('connection', ws => {
  console.log('✅ WebSocket 连接成功');

  let lastMessage = null;

  const interval = setInterval(() => {
    const start = Date.now();
    ws.send(JSON.stringify({ type: 'ping', timestamp: start }));
  }, 1000);

  ws.on('message', msg => {
    lastMessage = msg;
    try {
      const data = JSON.parse(msg);
      if (data.type === 'pong') {
        const latency = Date.now() - data.timestamp;
        ws.send(JSON.stringify({ type: 'latency', latency }));
      }
    } catch (e) {
      console.log('收到非 JSON 消息:', msg);
    }
  });

  ws.on('close', (code, reason) => {
    clearInterval(interval);
    console.log('❌ WebSocket 连接关闭');
    console.log(`关闭代码: ${code}`);
    console.log(`关闭原因: ${reason.toString()}`);
    if (lastMessage) {
      console.log(`最后收到的消息: ${lastMessage}`);
    } else {
      console.log('未收到任何消息');
    }
  });
});

server.listen(PORT, () => {
  console.log(`🌐 服务运行在 http://localhost:${PORT}`);
});
