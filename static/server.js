const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

// Проксируем запросы к API Новой почты
app.use('/novapost', createProxyMiddleware({
  target: 'https://api.novaposhta.ua',
  changeOrigin: true,
  followRedirects: true,
  pathRewrite: {
    '^/novapost': '',  // Убираем префикс /novapost
  },
}));

// Добавьте обработку остальных запросов, если необходимо
app.use(express.static('public'));  // Замените 'public' на путь к вашим статическим файлам
app.use(express.json());

// Запуск сервера
const port = process.env.PORT || 5000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
