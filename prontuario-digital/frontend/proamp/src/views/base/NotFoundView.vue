<template>
    <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div class="card max-w-md mx-auto text-center">
            <div class="text-gray-400 mb-4">
                <i class="fas fa-search text-6xl"></i>
            </div>
            <h1 class="text-2xl font-lato-bold text-gray-900 mb-2">Página Não Encontrada</h1>
            <p class="text-gray-600 font-lato-regular mb-6">A página que você está procurando não existe.</p>
            <div class="space-y-3">
                <router-link :to="{ name: 'admin-dashboard' }" class="btn-primary w-full"> Ir para Dashboard </router-link>
                <button @click="$router.go(-1)" class="btn-outline w-full">Voltar</button>
            </div>
        </div>
    </div>
</template>
