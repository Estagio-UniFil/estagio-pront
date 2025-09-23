# Guia de Uso dos Layouts Genéricos

## Estrutura dos Layouts

A refatoração criou uma estrutura modular e reutilizável para os layouts:

```
src/
├── components/
│   ├── layouts/
│   │   ├── BaseLayout.vue          # Layout base genérico
│   │   ├── AdminLayout.vue         # Layout específico do admin
│   │   ├── ManagerLayout.vue       # Layout específico do gestor
│   │   └── HealthProfessionalLayout.vue # Layout específico do profissional
│   └── common/
│       ├── Header.vue              # Header genérico (modificado)
│       └── Sidebar.vue             # Sidebar genérico (modificado)
└── config/
    └── layoutConfigs.js            # Configurações dos layouts
```

## Como Usar

### 1. AdminLayout (já existente - refatorado)

```vue
<template>
    <AdminLayout>
        <!-- Conteúdo da página admin -->
    </AdminLayout>
</template>

<script setup>
import AdminLayout from '@/components/layouts/AdminLayout.vue';
</script>
```

### 2. ManagerLayout (novo)

```vue
<template>
    <ManagerLayout>
        <!-- Conteúdo da página do gestor -->
    </ManagerLayout>
</template>

<script setup>
import ManagerLayout from '@/components/layouts/ManagerLayout.vue';
</script>
```

### 3. HealthProfessionalLayout (novo)

```vue
<template>
    <HealthProfessionalLayout>
        <!-- Conteúdo da página do profissional de saúde -->
    </HealthProfessionalLayout>
</template>

<script setup>
import HealthProfessionalLayout from '@/components/layouts/HealthProfessionalLayout.vue';
</script>
```

## Configurações

As configurações estão centralizadas em `src/config/layoutConfigs.js`:

- **Admin**: Dashboard, Usuários, Alunos, Relatórios
- **Manager**: Dashboard, Equipe, Alunos, Relatórios, Agenda
- **Health Professional**: Dashboard, Pacientes, Consultas, Prontuários, Agenda

## Personalização

Para adicionar novos itens de navegação ou modificar configurações:

1. Edite `src/config/layoutConfigs.js`
2. Adicione novas rotas no objeto `navigation`
3. Configure títulos e subtítulos nos mapas correspondentes

## Exemplo de Nova Configuração

```javascript
// Em layoutConfigs.js
newUserType: {
  containerClass: 'new-user-layout',
  mainContentClass: 'main-content lg:ml-64 lg:px-12',
  header: {
    title: 'Painel Personalizado',
    // ... outras configurações
  },
  sidebar: {
    title: 'ProAMP',
    subtitle: 'Personalizado',
    userRole: 'Usuário Personalizado',
    navigation: [
      {
        name: 'Dashboard',
        route: 'custom-dashboard',
        icon: 'fas fa-tachometer-alt'
      }
      // ... outros itens
    ]
  }
}
```

## Benefícios da Refatoração

1. **Reutilização**: Um layout base para todos os tipos de usuário
2. **Manutenibilidade**: Mudanças centralizadas no BaseLayout
3. **Configurabilidade**: Fácil adição de novos tipos de usuário
4. **Consistência**: Interface uniforme entre diferentes perfis
5. **Escalabilidade**: Estrutura preparada para crescimento
