# Pedido do investidor

### **Versão 1.0**

### Histórico de Revisão

| Data       | Versão | Descrição   | Autor     |
|------------|--------|-------------|-----------|
| 26/02/2025 | 1.0    | Primeira versão do documento | Luis Afonso Mineo |

---

## Introdução

### Objetivo

Este documento tem como objetivo capturar os requisitos e expectativas para o desenvolvimento de um prontuário digital destinado ao setor clínico da escola de educação especial Anna Maria Pietta, garantindo que o sistema atenda às necessidades reais dos profissionais de saúde e assistência social que trabalham na instituição.

### Escopo

O escopo deste documento abrange a coleta de requisitos para o desenvolvimento de um sistema de prontuário digital que permitirá o registro, acompanhamento e relatório de atendimentos realizados por profissionais de fisioterapia, fonoaudiologia, psicologia e assistência social na escola. O projeto impactará diretamente a eficiência do atendimento clínico e a gestão de informações dos alunos.

### Definições, Acrônimos e Abreviações

- **Prontuário Digital**: Sistema informatizado para registro de informações clínicas

### Referências

- Glossário
- [Artigo Prontuário eletrônico - gov.br](https://www.gov.br/saude/pt-br/composicao/saps/informatiza-aps/prontuario-eletronico)

### Visão Geral

Este documento apresenta o perfil dos usuários do sistema, avalia os problemas atuais, detalha o ambiente de uso, propõe soluções e estabelece critérios para avaliação de sucesso do projeto de prontuário digital para a escola de educação especial.

---

## Perfil do Investidor ou Usuário

**Nome:** Ivone Maria da Silva Mineo  
**Empresa / Segmento de Mercado:** Escola de Educação Especial / Educação e Saúde  
**Cargo:** Diretor  
**Responsabilidades principais:** Gestão da equipe pedagócia, gestão da equipe multidisciplinar de saúde  
**Distribuíveis produzidos:** Relatórios mensais de atendimento, evolução dos alunos, documentação para órgãos reguladores  
**Critérios de sucesso:** Melhoria no tempo de atendimento, redução de erros de registro, facilidade na geração de relatórios  
**Principais desafios:** Gerenciar informações de múltiplos profissionais, manter histórico de atendimentos organizados, gerar relatórios coerentes, garantir a privacidade dos dados  
**Tendências relevantes:** Digitalização de serviços de saúde, integração de equipes multidisciplinares, prontuários eletrônicos acessíveis  

---

## Avaliação do Problema

- **Problemas atuais sem boas soluções:**
  - **Registro manual de atendimentos:**
    - Os profissionais de saúde registram os atendimentos em formulários de papel, causando problemas de armazenamento, acesso e eventual perda de informações.
    - Solução proposta: Sistema digital de registro com acesso controlado por perfil de usuário.

  - **Dificuldade na consolidação de informações:**
    - No final do mês, é necessário revisar manualmente todos os registros para gerar relatórios, consumindo tempo significativo dos profissionais.
    - Solução proposta: Geração automática de relatórios mensais com contagem de alunos atendidos e listagem.

---

## Entendimento do Ambiente do Usuário

- **Quem são os usuários?**
  Profissionais de fisioterapia, fonoaudiologia, psicologia e assistência social que trabalham na escola.

- **Background educacional:**
  Graduação completa nas respectivas áreas, alguns com especialização em educação especial ou áreas correlatas.

- **Background tecnológico:**
  Familiaridade básica com computadores, mas variável dependendo da faixa etária e experiência individual.

- **Experiência com o tipo de aplicativo:**
  Experiência limitada ou inexistente com sistemas de prontuário digital.

- **Plataformas utilizadas:**
  Computadores desktop/notebooks na escola e eventualmente smartphones para consultas rápidas.

- **Planos futuros para plataformas:**
  Possibilidade de expansão para aplicativo móvel.

- **Aplicativos adicionais em uso:**
  Pacote Office (principalmente Word e Excel), aplicativos de comunicação (WhatsApp para equipe).

- **Expectativas de usabilidade:**
  Interface intuitiva, fluxo de trabalho simplificado, tempo mínimo para inserção de dados durante ou após o atendimento.

- **Expectativas de tempo de treinamento:**
  Máximo de 1 dia de treinamento inicial.

- **Necessidades de documentação:**
  Manual do usuário com instruções passo a passo, e suporte online ou presencial.

---

## Recapitulação para Entendimento

Os principais problemas enfrentados pela equipe clínica da escola de educação especial são: o registro manual de prontuários que dificulta o acesso e compartilhamento de informações e a dificuldade em gerar relatórios mensais consolidados que consomem tempo significativo da equipe. O sistema proposto visa solucionar esses problemas através de um prontuário digital integrado, seguro e com recursos de relatórios automatizados.

---

## Entradas do Analista

Quais, se houver, problemas estão associados com:

### **Problema 1: Registro manual dos atendimentos clínicos**

- **Este é um problema real?**
Sim, compromete a eficiência.

- **Quais são os motivos para este problema?**
Ausência de sistema digital.

- **Como você resolve o problema atualmente?**
Uso de formulários em papel armazenados em pastas físicas.

- **Como você gostaria de resolver o problema?**
Sistema digital centralizado com acesso por perfil profissional.

- **Como você classificaria a resolução desse problema?**
Prioridade alta, impacta diretamente a qualidade do atendimento.

### **Problema 2: Processo manual de consolidação de relatórios mensais**

- **Este é um problema real?**
Sim, consome tempo excessivo e gera riscos de erros estatísticos.

- **Quais são os motivos para este problema?**
Falta de automação e necessidade de revisar registros físicos.

- **Como você resolve o problema atualmente?**
Contagem manual.

- **Como você gostaria de resolver o problema?**
Geração automática de relatórios.

- **Como você classificaria a resolução desse problema?**
Prioridade alta, liberaria tempo significativo dos profissionais.

---

## Avaliação da Solução Proposta

A solução de prontuário digital proposta para a escola de educação especial contempla:

1. **Sistema de cadastro de alunos**: Permite o registro detalhado dos alunos com suas informações pessoais e necessidades específicas. (Importância: Alta)

2. **Prontuário por especialidade**: Cada área (fisioterapia, fonoaudiologia, psicologia e assistência social) terá campos específicos para registro dos atendimentos, mantendo a particularidade de cada especialidade. (Importância: Alta)

3. **Histórico integrado**: Visualização do histórico completo de atendimentos do aluno por todas as especialidades. (Importância: Média)

4. **Geração automática de relatórios**: Funcionalidade para gerar relatórios mensais com contagem de atendimentos e listagem dos alunos atendidos. (Importância: Alta)

5. **Controle de acesso e segurança**: Sistema de login e permissões por perfil de usuário, garantindo a confidencialidade dos dados. (Importância: Alta)

6. **Interface responsiva**: Adaptação para uso em diferentes dispositivos, caso necessário. (Importância: Baixa)

---

## Avaliação da Oportunidade

- **Necessidade do aplicativo na organização:**
  Extremamente necessário para modernizar e otimizar o processo de registro e acompanhamento clínico dos alunos, além de facilitar a geração de relatórios e estatísticas.

- **Número de usuários previstos:**
  4 profissionais das áreas de fisioterapia, fonoaudiologia, psicologia e assistência social, e 2 gestores.

- **Critérios para uma solução bem-sucedida:**
  - Redução no tempo gasto com registros manuais
  - Eliminação de erros na contagem de atendimentos mensais
  - Feedback positivo dos usuários quanto à usabilidade
  - Conformidade com requisitos de segurança e privacidade

---

## Avaliação de Confiabilidade, Desempenho e Suporte

- **Expectativas de confiabilidade:**
  Disponibilidade durante o horário de funcionamento da escola, das 07:30 às 17:25 horas.

- **Expectativas de desempenho:**
  Tempo de resposta rápido, e aplicação flúida.

- **Necessidades de suporte:**
  Suporte técnico disponível durante horário comercial.

- **Requisitos de segurança:**
  Controle de acesso por perfil, registro de logs de atividades.

- **Requisitos de instalação e configuração:**
  Sistema baseado em web, sem necessidade de instalação nos computadores clientes, apenas configuração inicial do servidor e cadastro dos usuários.

- **Requisitos de licenciamento:**
  Licença por número de usuários ativos, com modelo de assinatura anual ou aquisição permanente a ser definido.

- **Métodos de distribuição:**
  Acesso via navegador web com credenciais institucionais.

---

## Conclusão

O desenvolvimento de um sistema de prontuário digital para o setor clínico da escola de educação especial Anna Maria Pietta é uma oportunidade para modernizar os processos de atendimento e otimizar o tempo dos profissionais.

---

## Resumo do Analista

1. **Problema 1:** Registro manual dos atendimentos clínicos, resultando em ineficiência e risco de perda de informações.

2. **Problema 2:** Processo manual e demorado de consolidação de relatórios mensais sobre quantidade de atendimentos e alunos atendidos.

---

## Wrap-up

- **Se eu precisar fazer outras perguntas, posso telefonar para você?**
  Sim, pessoalmente ou Whatsapp.

- **Você estaria disposto a participar de uma revisão de requisitos?**
  Sim, a qualquer momento.

---

**Versão:** 1.0  
**Data:** 26/02/2025  
**Empresa:** Associação de Pais e Amigos dos Excepcionais de Florestópolis / Escola de educação especial Anna Maria Pietta  
**Confidencialidade:** Confidencial  
**Copyright:** © Associação de Pais e Amigos dos Excepcionais de Florestópolis 2025  

---
