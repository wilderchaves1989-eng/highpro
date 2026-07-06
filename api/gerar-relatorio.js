// Endpoint serverless para Vercel - Gera PDF de Performance
const PDFDocument = require('pdfkit');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const dados = req.body;
    const { nome, cargo, email, telefone, media, skills = {}, avaliacao = {} } = dados;

    // Criar PDF
    const doc = new PDFDocument();
    const chunks = [];

    doc.on('data', chunk => chunks.push(chunk));
    doc.on('end', () => {
      const pdfBuffer = Buffer.concat(chunks);
      res.setHeader('Content-Type', 'application/pdf');
      res.setHeader('Content-Disposition', `attachment; filename="${nome.replace(/\\s+/g, '_')}_performance.pdf"`);
      res.send(pdfBuffer);
    });

    // Header
    doc.fontSize(20).fillColor('#0564FF').text('HIGH PRO', { align: 'left' });
    doc.fontSize(12).fillColor('#5A5A5A').text('SOLUTIONS', { align: 'left' });
    doc.fontSize(10).fillColor('#5A5A5A').text(`Relatório de Performance | ${new Date().toLocaleDateString('pt-PT')}`, { align: 'right', moved: true });
    doc.moveTo(50, 80).lineTo(550, 80).stroke('#E8ECF2');
    doc.moveDown();

    // Dados do Colaborador
    doc.fontSize(12).fillColor('#1A1A1A').text('Dados do Colaborador', { underline: true });
    doc.fontSize(10);
    doc.text(`Nome: ${nome}`);
    doc.text(`Cargo: ${cargo || '—'}`);
    doc.text(`Email: ${email || '—'}`);
    doc.text(`Telemóvel: ${telefone || '—'}`);
    doc.moveDown();

    // Avaliação Geral
    doc.fontSize(12).fillColor('#1A1A1A').text('Avaliação Geral', { underline: true });
    doc.fontSize(10);
    const statusTxt = media >= 67 ? 'Excelente' : (media >= 33 ? 'Bom' : 'Crítico');
    const statusCor = media >= 67 ? '#10B981' : (media >= 33 ? '#F59E0B' : '#EF4444');
    doc.fillColor(statusCor).text(`Pontuação Geral: ${media}/100 - ${statusTxt}`);
    doc.moveDown();

    // Competências
    doc.fontSize(12).fillColor('#1A1A1A').text('Competências Profissionais', { underline: true });
    doc.fontSize(9);
    Object.entries(skills).forEach(([skill, pontos]) => {
      const skillStatus = pontos < 33 ? 'Crítico' : (pontos < 67 ? 'Em Desenv.' : 'Forte');
      doc.text(`• ${skill}: ${pontos}% (${skillStatus})`);
    });
    doc.moveDown();

    // Matriz de Performance
    doc.fontSize(12).fillColor('#1A1A1A').text('Matriz de Performance', { underline: true });
    doc.fontSize(10);
    const matriz = avaliacao.matrizQuadrantes || {};
    doc.text(`Força: ${matriz.forca || 0}`);
    doc.text(`Oportunidade: ${matriz.oportunidade || 0}`);
    doc.text(`Fraqueza: ${matriz.fraqueza || 0}`);
    doc.text(`Ameaça: ${matriz.ameaca || 0}`);
    doc.moveDown();

    // Footer
    doc.fontSize(8).fillColor('#8A8A8A').text(
      'HIGH PRO Solutions • Controlo de Horas © 2026 • Todos os direitos reservados',
      { align: 'center', margin: 50 }
    );

    // Finalizar PDF
    doc.end();

  } catch (error) {
    console.error('Erro ao gerar PDF:', error);
    res.status(500).json({ error: 'Erro ao gerar relatório', details: error.message });
  }
};
