const express = require('express');
const { MongoClient } = require('mongodb');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');
const os = require('os');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// MongoDB Connection String (definir em variável de ambiente MONGODB_URI)
const MONGODB_URI = process.env.MONGODB_URI;
if (!MONGODB_URI) { console.error('MONGODB_URI não definida. Configure a variável de ambiente.'); process.exit(1); }
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

// POST - Gerar Relatório PDF de Performance
app.post('/api/gerar-relatorio', (req, res) => {
  try {
    const dados = req.body;
    const tempDir = os.tmpdir();
    const tempFile = path.join(tempDir, `relatorio_${Date.now()}.pdf`);

    // Preparar dados para o Python
    const jsonData = JSON.stringify(dados);

    // Criar script Python temporário que gera o PDF
    const pythonScript = `
import sys
import json
import os
sys.path.insert(0, '${path.join(__dirname).replace(/\\\\/g, '\\\\\\\\')}')

from gerar_relatorio_pdf import RelatorioPerformance

# Ler dados do stdin
dados = json.loads('''${jsonData}''')

# Gerar PDF
relatorio = RelatorioPerformance(dados)
relatorio.gerar_pdf('${tempFile.replace(/\\\\/g, '\\\\\\\\')}')
print("OK")
`;

    // Executar Python
    const python = spawn('python', ['-c', pythonScript], { cwd: __dirname });
    let output = '';
    let error = '';

    python.stdout.on('data', (data) => {
      output += data.toString();
    });

    python.stderr.on('data', (data) => {
      error += data.toString();
    });

    python.on('close', (code) => {
      if (code === 0 && fs.existsSync(tempFile)) {
        // Enviar PDF
        res.setHeader('Content-Type', 'application/pdf');
        res.setHeader('Content-Disposition', `attachment; filename="${dados.nome.replace(/\\s+/g, '_')}_performance.pdf"`);
        const fileStream = fs.createReadStream(tempFile);

        fileStream.pipe(res);

        // Deletar arquivo após envio
        fileStream.on('end', () => {
          try { fs.unlinkSync(tempFile); } catch (e) {}
        });
      } else {
        console.error('Erro ao gerar PDF:', error || output);
        res.status(500).json({ error: 'Erro ao gerar relatório', details: error });
      }
    });
  } catch (error) {
    console.error('Erro:', error);
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
