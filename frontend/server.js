const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

// Proxy API requests to the backend
app.use('/api', createProxyMiddleware({ 
  target: 'http://localhost:8000'
}));

// Serve static files
app.use(express.static('build'));

// Handle React routing
app.get('*', function(req, res) {
  res.sendFile('build/index.html', { root: __dirname });
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
