// Layout config for each user type

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
                'manager-reports': 'Relatórios',
            },
            subtitleMap: {
                'manager-dashboard': 'Bem vindo, {name}!',
                'manager-team': 'Gestão > Equipe',
                'manager-reports': 'Gestão > Relatórios',
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
                    name: 'Relatórios',
                    route: 'manager-reports',
                    icon: 'fas fa-chart-line',
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
                'health-students': 'Estudantes',
                'health-records': 'Prontuários',
                'health-reports': 'Relatórios',
            },
            subtitleMap: {
                'health-dashboard': 'Bem vindo, {name}!',
                'health-students': 'Atendimento > Estudantes',
                'health-records': 'Atendimento > Prontuários',
                'health-reports': 'Atendimento > Relatórios',
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
                    name: 'Estudantes',
                    route: 'health-students',
                    icon: 'fas fa-user-injured',
                },
                {
                    name: 'Prontuários',
                    route: 'health-records',
                    icon: 'fas fa-file-medical',
                },
                {
                    name: 'Relatórios',
                    route: 'health-reports',
                    icon: 'fas fa-chart-bar',
                },
            ],
        },
    },
};

// Helper by user type
export const getLayoutConfig = (userType) => {
    return layoutConfigs[userType] || layoutConfigs.admin;
};
