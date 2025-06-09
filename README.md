# ProAMP - Prontuário Digital

Sistema de prontuário digital desenvolvido para o setor clínico da escola de educação especial Anna Maria Pietta, visando otimizar a gestão de atendimentos e automatizar a geração de relatórios.

## 📋 Sobre o Projeto

O ProAMP é um sistema web que digitaliza o processo de registro de atendimentos clínicos, substituindo o método manual por uma solução automatizada que garante maior precisão, agilidade e conformidade com os requisitos do convênio SUS.

### Objetivos Principais

- Facilitar o registro eletrônico de atendimentos
- Automatizar a geração de relatórios mensais
- Otimizar processos administrativos

## 🏗️ Arquitetura

**Backend:** Python 3.12.4 + Django 5.2 + Django REST Framework 3.16.0  
**Banco de Dados:** PostgreSQL 17  
**Frontend:** JavaScript Puro (migração para React/Vue em análise)

## 📁 Estrutura do Repositório

```
estagio-pront/  
├── .github/workflows/          # CI/CD workflows  
├── docs/                       # Documentação do projeto  
│   ├── arquivos/              # Documentos gerais (Plano de Estágio)
│   ├── artefatos/             # Artefatos (Documentação RUP/UML)  
│   ├── casos_de_uso/          # Especificações de casos de uso  
│   │   └── gerenciamento-de-alunos/  
│   └── diagramas/             # Diagramas técnicos  
│       └── svg/               # Diagramas em formato SVG  
└── prontuario-digital/  
    └── backend/               # Código do backend Django  
```

## 📚 Documentação

### Artefatos de Engenharia

- **[Plano de Estágio](docs/arquivos/v2proamp-plano-de-estagio.pdf)** - Documento completo do projeto
- **[Glossário do Projeto](docs/artefatos/0-art-glossario-projeto.pdf)** - Termos técnicos e definições
- **[Pedido do Investidor](docs/artefatos/1-art-pedido-investidor.pdf)** - Solicitação inicial
- **[Especificação Suplementar](docs/artefatos/2-art-espec-suplementar.pdf)** - Requisitos não funcionais
- **[Documento de Visão](docs/artefatos/3-art-visao.pdf)** - Visão geral e objetivos

### Casos de Uso

- **[Gerenciamento de Alunos](docs/casos_de_uso/gerenciamento-de-alunos/)** - Especificação detalhada

### Diagramas

Todos os diagramas estão disponíveis em **[docs/diagramas/](docs/diagramas/0-diagramas-merged.pdf)**:

- **Diagrama de Classes** - Estrutura orientada a objetos
- **Diagrama ER** - Modelo conceitual do banco
- **Diagrama Lógico** - Implementação física do banco
- **Diagrama de Sequência** - Fluxos de interação
- **Diagrama de Estados** - Ciclo de vida dos registros
- **Diagrama de Implantação** - Arquitetura de distribuição

## 👥 Funcionalidades por Perfil

### Administrador

- Gerenciamento de alunos e funcionários
- Acesso completo ao sistema

### Setor Clínico

- Registro de atendimentos
- Consulta de histórico de pacientes
- Geração de relatórios mensais

### Gestores

- Visualização de histórico de atendimentos
- Acesso a relatórios

## 🔗 Links Úteis

- **Repositório de Documentação:** [luismineo.github.io/proamp-docs](https://luismineo.github.io/proamp-docs/)
- **Glossário Interativo:** [luismineo.github.io/proamp-docs](https://luismineo.github.io/proamp-docs/pages/glossario.html)

---

**Orientando:** Luis Afonso Mineo <br>
**Orientador:** Ricardo Petri Silva <br>
**Curso:** Bacharelado em Ciência da Computação <br>
**Ano:** 2025
