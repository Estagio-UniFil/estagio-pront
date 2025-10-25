<template>
    <div class="dashboard-container">
        <!-- Sidebar -->
        <div class="sidebar">
            <div class="sidebar-header">
                <h1 class="sidebar-title">Prontuário Digital</h1>
            </div>

            <nav class="p-4">
                <a href="#" class="nav-link active">
                    <span>Dashboard</span>
                </a>
                <a href="#" class="nav-link">
                    <span>Funcionários</span>
                </a>
                <a href="#" class="nav-link">
                    <span>Alunos</span>
                </a>
                <a href="#" class="nav-link">
                    <span>Relatórios</span>
                </a>
            </nav>
        </div>

        <!-- Main Content -->
        <div class="main-content">
            <!-- Header -->
            <div class="flex justify-between items-center mb-8">
                <div>
                    <h1 class="text-3xl font-lato-black text-gray-900">Teste de Estilizações</h1>
                    <p class="text-gray-600 font-lato-regular mt-2">Visualização da identidade visual do sistema</p>
                </div>
                <button class="btn-primary">Novo Cadastro</button>
            </div>

            <!-- Cards Section -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Total de Alunos</h3>
                        <p class="card-subtitle">Alunos ativos no sistema</p>
                    </div>
                    <div class="text-3xl font-lato-black text-blue-600">127</div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Funcionários</h3>
                        <p class="card-subtitle">Profissionais cadastrados</p>
                    </div>
                    <div class="text-3xl font-lato-black text-green-600">23</div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Consultas Hoje</h3>
                        <p class="card-subtitle">Atendimentos realizados</p>
                    </div>
                    <div class="text-3xl font-lato-black text-purple-600">8</div>
                </div>
            </div>

            <!-- Buttons Section -->
            <div class="card mb-8">
                <div class="card-header">
                    <h3 class="card-title">Botões do Sistema</h3>
                    <p class="card-subtitle">Diferentes estilos de botões disponíveis</p>
                </div>

                <div class="flex flex-wrap gap-4">
                    <button class="btn-primary">Botão Primário</button>
                    <button class="btn-secondary">Botão Secundário</button>
                    <button class="btn-danger">Botão Perigo</button>
                    <button class="btn-outline">Botão Outline</button>
                </div>
            </div>

            <!-- Form Section -->
            <div class="card mb-8">
                <div class="card-header">
                    <h3 class="card-title">Formulário de Exemplo</h3>
                    <p class="card-subtitle">Campos de entrada com estilização personalizada</p>
                </div>

                <form class="space-y-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label class="input-label">Nome Completo</label>
                            <input type="text" class="input-field" placeholder="Digite o nome completo" />
                        </div>

                        <div>
                            <label class="input-label">E-mail</label>
                            <input type="email" class="input-field" placeholder="exemplo@email.com" />
                        </div>
                    </div>

                    <div>
                        <label class="input-label">Função</label>
                        <select class="input-field">
                            <option>Selecione uma função</option>
                            <option>Administrador</option>
                            <option>Psicólogo</option>
                            <option>Fisioterapeuta</option>
                        </select>
                    </div>

                    <div class="flex gap-4">
                        <button type="submit" class="btn-primary">Salvar</button>
                        <button type="button" class="btn-secondary">Cancelar</button>
                    </div>
                </form>
            </div>

            <!-- Table Section -->
            <div class="card mb-8">
                <div class="card-header">
                    <h3 class="card-title">Lista de Funcionários</h3>
                    <p class="card-subtitle">Exemplo de tabela com dados</p>
                </div>

                <table class="table">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>E-mail</th>
                            <th>Função</th>
                            <th>Status</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="font-lato-bold">Maria Silva</td>
                            <td>maria@escola.com</td>
                            <td>Psicóloga</td>
                            <td><span class="badge badge-success">Ativo</span></td>
                            <td>
                                <button class="btn-secondary text-xs py-1 px-2">Editar</button>
                            </td>
                        </tr>
                        <tr>
                            <td class="font-lato-bold">João Santos</td>
                            <td>joao@escola.com</td>
                            <td>Fisioterapeuta</td>
                            <td><span class="badge badge-success">Ativo</span></td>
                            <td>
                                <button class="btn-secondary text-xs py-1 px-2">Editar</button>
                            </td>
                        </tr>
                        <tr>
                            <td class="font-lato-bold">Ana Costa</td>
                            <td>ana@escola.com</td>
                            <td>Fonoaudióloga</td>
                            <td><span class="badge badge-warning">Inativo</span></td>
                            <td>
                                <button class="btn-secondary text-xs py-1 px-2">Editar</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Alerts Section -->
            <div class="space-y-4 mb-8">
                <div class="alert alert-success"><strong>Sucesso!</strong> Funcionário cadastrado com sucesso.</div>
                <div class="alert alert-warning"><strong>Atenção!</strong> Alguns campos precisam ser preenchidos.</div>
                <div class="alert alert-error"><strong>Erro!</strong> Não foi possível salvar os dados.</div>
                <div class="alert alert-info"><strong>Informação:</strong> Sistema será atualizado em breve.</div>
            </div>

            <!-- Typography Section -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Tipografia Lato</h3>
                    <p class="card-subtitle">Diferentes pesos da fonte</p>
                </div>

                <div class="space-y-4">
                    <p class="font-lato-thin text-lg">Lato Thin (100) - Texto muito leve</p>
                    <p class="font-lato-light text-lg">Lato Light (300) - Texto leve</p>
                    <p class="font-lato-regular text-lg">Lato Regular (400) - Texto normal</p>
                    <p class="font-lato-bold text-lg">Lato Bold (700) - Texto em negrito</p>
                    <p class="font-lato-black text-lg">Lato Black (900) - Texto muito pesado</p>
                </div>
            </div>
        </div>

        <!-- Loading Spinner (hidden by default) -->
        <div class="fixed bottom-4 right-4">
            <div class="loading-spinner"></div>
        </div>
    </div>
</template>

<script setup></script>
