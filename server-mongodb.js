const express = require('express');
const { MongoClient } = require('mongodb');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// MongoDB Connection String
const MONGODB_URI = 'mongodb+srv://HIGHPRO:HIGHPRO2602@cluster0.e6wgpy6.mongodb.net/highpro?retryWrites=true&w=majority';
const client = new MongoClient(MONGODB_URI);
let db = null;

// Conectar ao MongoDB
async function connectMongoDB() {
  try {
    await client.connect();
    db = client.db('highpro');
    console.log('✅ MongoDB conectado com sucesso!');
  } catch (error) {
    console.log('⚠️ Erro ao conectar MongoDB:');
    console.log('   ', error.message);
  }
}

connectMongoDB();

// Middleware
app.use(express.json({ limit: '50mb' }));
app.use(express.static(path.join(__dirname, '.')));

// Rotas API

// GET - Carregar dados
app.get('/api/dados', async (req, res) => {
  try {
    if (!db) return res.status(503).json({ error: 'MongoDB não conectado' });

    const doc = await db.collection('dados').findOne({ _id: 'global' });
    if (doc) {
      res.json({ colaboradores: doc.colaboradores || [], horas: doc.horas || {} });
    } else {
      res.json({ colaboradores: [], horas: {} });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// POST - Salvar dados
app.post('/api/dados', async (req, res) => {
  try {
    if (!db) return res.status(503).json({ error: 'MongoDB não conectado' });

    const { colaboradores, horas } = req.body;
    await db.collection('dados').updateOne(
      { _id: 'global' },
      { $set: { colaboradores, horas, timestamp: new Date() } },
      { upsert: true }
    );

    res.json({ success: true, message: 'Dados salvos com sucesso' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// GET - Serve HTML principal
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'high-pro-app.html'));
});

// Iniciar servidor
app.listen(PORT, () => {
  console.log(`\n🚀 HIGH PRO Server rodando em http://localhost:${PORT}`);
  console.log(`📁 Ficheiro: ${path.join(__dirname, 'high-pro-app.html')}\n`);
});

// Graceful shutdown
process.on('SIGINT', async () => {
  await client.close();
  process.exit(0);
});
