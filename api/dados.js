const { MongoClient } = require('mongodb');

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb+srv://HIGHPRO:HIGHPRO2602@cluster0.e6wgpy6.mongodb.net/highpro?retryWrites=true&w=majority';

let cachedClient = null;

async function connectToDatabase() {
  if (cachedClient) {
    return cachedClient;
  }

  const client = new MongoClient(MONGODB_URI);
  await client.connect();
  cachedClient = client;
  return client;
}

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  try {
    const client = await connectToDatabase();
    const db = client.db('highpro');

    if (req.method === 'GET') {
      const doc = await db.collection('dados').findOne({ _id: 'global' });
      if (doc) {
        res.json({ colaboradores: doc.colaboradores || [], horas: doc.horas || {} });
      } else {
        res.json({ colaboradores: [], horas: {} });
      }
    } else if (req.method === 'POST') {
      const { colaboradores, horas } = req.body;
      await db.collection('dados').updateOne(
        { _id: 'global' },
        { $set: { colaboradores, horas, timestamp: new Date() } },
        { upsert: true }
      );
      res.json({ success: true, message: 'Dados salvos com sucesso' });
    }
  } catch (error) {
    console.error('API Error:', error);
    res.status(500).json({ error: error.message, details: process.env.MONGODB_URI ? 'URI set' : 'URI missing' });
  }
};
