# HIGH PRO — Roteiro de Melhorias

Revisão de estado e plano de evolução. Atualizado em 2026-07-05.

## Estado atual (o que já funciona)

- Controlo de horas por colaborador (trabalhadas, faltas, feriados, atestados)
- Cálculo de extras: 50% (dias úteis acima de 8h) e 100% (sábados/feriados) para contrato fixo
- Contratos: Fixo de Portugal e Termo Incerto
- Fichas de colaborador com 4 abas: Perfil, Dados, Movimentações, Skills
- Fotos com compressão automática (máx. 300px)
- Exportações: PDF e Excel (individual e geral), CSV para Google Sheets, Backup/Restauro JSON
- Modal de registos (ver, editar, apagar, lançar)
- Arquivar/desarquivar colaboradores
- Reordenar cards por arrastar (estilo Trello)
- Envio de comprovativo por WhatsApp (semi-automático, via wa.me)
- Design estilo Nexora, fonte General Sans, responsivo (telemóvel a 1 coluna)
- Backend MongoDB no Vercel, com fallback para localStorage

## QA (2026-07-05)

20/20 testes funcionais passaram. Cálculos de extras corretos, validações a funcionar
(nome curto e hora futura rejeitados), XSS escapado, sem overflow em telemóvel.
Sistema sólido para o uso atual.

## Melhorias prioritárias

### Crítico — Segurança
1. **Rotacionar a senha do MongoDB.** A senha esteve escrita no código e continua no
   histórico do Git. Ação manual do utilizador no MongoDB Atlas + variável de ambiente
   no Vercel. Depois, remover o fallback com senha em `api/dados.js`.
2. **Adicionar autenticação.** Hoje qualquer pessoa com o link vê e edita horas e
   salários. Mínimo: uma senha de acesso; ideal: acesso por perfil.

### Importante — Integridade de dados
3. **Gravação por colaborador.** Hoje cada gravação sobrescreve o bloco global inteiro;
   duas edições simultâneas causam perda de dados (último a gravar vence).
4. **Aviso de modo offline.** Quando a API falha, o sistema usa dados locais antigos sem
   avisar. Mostrar aviso visível.

### Otimização — Desempenho e limpeza
5. **Remover Firebase.** 4 scripts carregados mas não usados (dados vêm do MongoDB).
   Site abre mais rápido sem eles.
6. **Separar horas por colaborador.** Tudo está num só documento (limite 16 MB, tudo
   descarregado a cada visita). Só necessário quando os dados crescerem (~2-3 MB).

## Capacidade no plano grátis atual

- Limite real: 16 MB por documento MongoDB (não os 512 MB do plano)
- ~200.000 registos de horas no total (décadas de uso para equipa pequena)
- Colaboradores: milhares sem foto; algumas centenas com foto (~15 KB cada)
- Vercel: ~200 KB por visita, dá para centenas de milhares de visitas/mês
- Conclusão: praticamente ilimitado para o uso atual
