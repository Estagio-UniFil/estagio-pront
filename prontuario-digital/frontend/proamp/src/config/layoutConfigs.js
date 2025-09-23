// Configurações específicas para cada tipo de layout

export const layoutConfigs = {
    admin: {
        containerClass: 'admin-layout',
        mainContentClass: 'main-content lg:ml-64 lg:px-12',
        header: {
            title: 'Painel de administrador',
            showSearch: false,
            userRole: 'admin',
            routeMap: {
                'admin-dashboard': 'Dashboard',
                'admin-users': 'Funcionários',
                'admin-students': 'Alunos',
                'admin-reports': 'Relatórios',
                'admin-settings': 'Configurações',
            },
            subtitleMap: {
                'admin-dashboard': 'Bem vindo, {name}!',
                'admin-users': 'Admin > Usuários',
                'admin-students': 'Admin > Alunos',
                'admin-reports': 'Admin > Relatórios',
                'admin-settings': 'Admin > Configurações',
            },
        },
        sidebar: {
            title: 'ProAMP',
            subtitle: 'Administração',
            userRole: 'Administrador',
            navigation: [
                {
                    name: 'Dashboard',
                    route: 'admin-dashboard',
                    icon: 'fas fa-tachometer-alt',
                    active: true,
                },
                {
                    name: 'Usuários',
                    route: 'admin-users',
                    icon: 'fas fa-user-md',
                },
                {
                    name: 'Alunos',
                    route: 'admin-students',
                    icon: 'fas fa-users',
                },
                {
                    name: 'Relatórios',
                    route: 'admin-reports',
                    icon: 'fas fa-chart-bar',
                },
            ],
        },
    },

    manager: {
        containerClass: 'manager-layout',
        mainContentClass: 'main-content lg:ml-64 lg:px-12',
        header: {
            title: 'Painel do gestor',
            showSearch: true,
            userRole: 'manager',
            routeMap: {
                'manager-dashboard': 'Dashboard',
                'manager-team': 'Equipe',
                'manager-students': 'Alunos',
                'manager-reports': 'Relatórios',
                'manager-schedule': 'Agenda',
            },
            subtitleMap: {
                'manager-dashboard': 'Bem vindo, {name}!',
                'manager-team': 'Gestão > Equipe',
                'manager-students': 'Gestão > Alunos',
                'manager-reports': 'Gestão > Relatórios',
                'manager-schedule': 'Gestão > Agenda',
            },
        },
        sidebar: {
            title: 'ProAMP',
            subtitle: 'Gestão',
            userRole: 'Gestor',
            navigation: [
                {
                    name: 'Dashboard',
                    route: 'manager-dashboard',
                    icon: 'fas fa-tachometer-alt',
                },
                {
                    name: 'Equipe',
                    route: 'manager-team',
                    icon: 'fas fa-users',
                },
                {
                    name: 'Alunos',
                    route: 'manager-students',
                    icon: 'fas fa-graduation-cap',
                },
                {
                    name: 'Relatórios',
                    route: 'manager-reports',
                    icon: 'fas fa-chart-line',
                },
                {
                    name: 'Agenda',
                    route: 'manager-schedule',
                    icon: 'fas fa-calendar-alt',
                },
            ],
        },
    },

    'health-professional': {
        containerClass: 'health-professional-layout',
        mainContentClass: 'main-content lg:ml-64 lg:px-12',
        header: {
            title: 'Painel do profissional',
            showSearch: true,
            userRole: 'health-professional',
            routeMap: {
                'health-dashboard': 'Dashboard',
                'health-patients': 'Pacientes',
                'health-appointments': 'Consultas',
                'health-records': 'Prontuários',
                'health-schedule': 'Agenda',
            },
            subtitleMap: {
                'health-dashboard': 'Bem vindo, {name}!',
                'health-patients': 'Atendimento > Pacientes',
                'health-appointments': 'Atendimento > Consultas',
                'health-records': 'Atendimento > Prontuários',
                'health-schedule': 'Atendimento > Agenda',
            },
        },
        sidebar: {
            title: 'ProAMP',
            subtitle: 'Atendimento',
            userRole: 'Profissional de Saúde',
            navigation: [
                {
                    name: 'Dashboard',
                    route: 'health-dashboard',
                    icon: 'fas fa-tachometer-alt',
                },
                {
                    name: 'Pacientes',
                    route: 'health-patients',
                    icon: 'fas fa-user-injured',
                },
                {
                    name: 'Consultas',
                    route: 'health-appointments',
                    icon: 'fas fa-stethoscope',
                },
                {
                    name: 'Prontuários',
                    route: 'health-records',
                    icon: 'fas fa-file-medical',
                },
                {
                    name: 'Agenda',
                    route: 'health-schedule',
                    icon: 'fas fa-calendar-check',
                },
            ],
        },
    },
};

// Função helper para obter configuração por tipo de usuário
export const getLayoutConfig = (userType) => {
    return layoutConfigs[userType] || layoutConfigs.admin;
};
