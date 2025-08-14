<template>
    <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div class="card max-w-md mx-auto text-center">
            <div class="text-red-600 mb-4">
                <i class="fas fa-ban text-6xl"></i>
            </div>
            <h1 class="text-2xl font-lato-bold text-gray-900 mb-2">Acesso Negado</h1>
            <p class="text-gray-600 font-lato-regular mb-6">Você não tem permissão para acessar esta página.</p>
            <div class="space-y-3">
                <router-link :to="{ name: 'login' }" class="btn-primary w-full"> Fazer Login </router-link>
                <button @click="$router.go(-1)" class="btn-outline w-full">Voltar</button>
            </div>
        </div>
    </div>
</template>
