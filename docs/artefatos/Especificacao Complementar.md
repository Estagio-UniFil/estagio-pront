## Especificação Complementar

### **Versão 1.1**

### Histórico de Revisão

| Data       | Versão | Descrição   | Autor     |
|------------|--------|-------------|-----------|
| 26/02/2025 | 1.0    | Primeira versão do documento | Luis Afonso Mineo |
| 27/02/2025 | 1.1    | Correção de erros pontuais | Luis Afonso Mineo |

---

## Introdução

### Objetivo

Este documento detalha os requisitos complementares do sistema de prontuário digital destinado ao setor clínico da escola de educação especial Anna Maria Pietta.

### Escopo

A especificação complementar cobre os requisitos não funcionais e alguns aspectos técnicos.

### Definições, Acrônimos e Abreviações

- MVC: padrão de arquitetura de software que separa um aplicativo em três camadas: Model, View e Controller;
- HTTPS: Hypertext Transfer Protocol Secure;
- HTTP: Hypertext Transfer Protocol;
- PostgreSQL: Sistema de gerenciamento de banco de dados;
- CSV: Formato de arquivo usado em planilhas;
- MTTR: "Mean Time to Repair", ou tempo médio de reparos.

### Referências

- [Pedido do investidor](https://github.com/Estagio-UniFil/estagio-pront/wiki/Pedido-do-investidor)
- [Artigo Prontuário eletrônico - gov.br](https://www.gov.br/saude/pt-br/composicao/saps/informatiza-aps/prontuario-eletronico)

### Visão Geral

Este documento está organizado em seções, para detalhar requisitos não funcionais do projeto de prontuário eletrônico.

---

## Funcionalidade

### Registro Digital de Atendimentos

- Permitir que os profissionais de saúde registrem atendimentos eletronicamente;
- Data e hora do registro preenchidos de forma automática.

### Geração de Relatórios Automática

- Relatórios mensais de atendimento gerados automaticamente;
- Possibilidade de exportação em formatos PDF e CSV.

---

## Utilidade

### Facilidade de Uso

- Interface intuitiva e acessível;
- Tempo médio de aprendizado estimado: 1 dia de treinamento.

---

## Confiabilidade

- Disponibilidade do sistema durante o horário de funcionamento da escola (07:30 às 17:25);
- Tempo médio para correção de erros de até 24 horas (MTTR).

---

## Desempenho

- Tempo de resposta máximo de 30 segundos por requisição, acima disso será considerado falha;
- Capacidade de atender até 10 usuários simultâneos.

---

## Suportabilidade

- Suporte técnico disponível em horário comercial.

---

## Restrições de Design

- Desenvolvimento utilizando tecnologias web;
- Banco de dados PostgreSQL.

---

## Documentação do Usuário

- Manual do usuário disponibilizado online.

---

## Interfaces

### Interfaces com o Usuário

- Interface responsiva compatível com desktop e possivelmente dispositivos móveis.

### Interfaces de Hardware

- Hardware necessita acesso à internet e requisitos mínimos para abrir o navegador web.

### Interfaces de Software

- Desenvolvimento do sistema será através de ferramentas de desevolvimento web, com arquitetura MVC;
- Para gerenciamento de dados será usado PostgreSQL

### Interfaces de Comunicações

- Comunicação entre navegador do usuário e servidor via protocolo HTTPS/HTTP.

---

## Requisitos de Licença

- Não necessita de lincenças.

---

## Observações Legais

- Software é de uso interno, portanto sendo apenas acessível para profissionais cadastrados na instituição.

---

## Padrões Aplicáveis

- Na documentação, será baseado em diagramas UML e modelos retirados do RUP;
- No desenvolvimento, será voltado para padrões de desenvolvimento web, tanto na arquitetura, quanto no tratamento e segurança de dados.

---

**Versão:** 1.1  
**Data:** 27/02/2025  
**Empresa:** Associação de Pais e Amigos dos Excepcionais de Florestópolis  
**Confidencialidade:** Confidencial  
**Copyright:** © Associação de Pais e Amigos dos Excepcionais de Florestópolis 2025  

---

