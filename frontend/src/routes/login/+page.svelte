<script lang="ts">
	import { Register } from 'flowbite-svelte-blocks';
	import { Button, Checkbox, Label, Input } from 'flowbite-svelte';
	import { account } from '$lib/appwrite';

	let loggedInUser = null;
	
	export let data;
	
	// Auto-login
	async function redirectToSubscription() {
		const subscriptionUrl = 'subscriptions' + (data && data.id ? '?subscriptionId=' + encodeURIComponent(data.id) : '');
		window.location.href = subscriptionUrl;
	}

	async function check_session() {
		try {
			loggedInUser = await account.get();
			console.log(`User ${loggedInUser.email} is already logged in`);
			await redirectToSubscription();
		} catch (error) {
			console.error('Session check failed:', error);
		}
	}
	
	check_session();
	
	// Login
	async function login(email, password) {
		try {
			await account.createEmailSession(email, password);
			console.log("Inicio de sesión exitoso");
			await redirectToSubscription();
		} catch (error) {
			console.error('Login failed:', error);
			alert("Error iniciando sesión. Por favor verifique el email y la contraseña e intente nuevamente.")
		}
	}
	
	// Submit form handler
	function submit(e) {
		e.preventDefault();
		const formData = new FormData(e.target);
		login(formData.get('email'), formData.get('password'));
	}
</script>


<section class="relative flex flex-wrap lg:h-screen lg:items-center">
	<div class="relative h-64 w-full sm:h-96 lg:h-full lg:w-1/2">
		<img alt="Welcome" src="../form_image.jpg" class="absolute inset-0 h-full w-full object-cover" />
	</div>
	<div class="w-full px-4 py-12 sm:px-6 sm:py-16 lg:w-1/2 lg:px-8 lg:py-24">
		<Register>
			<div class="p-6 space-y-4 md:space-y-6 sm:p-8">
				<form class="flex flex-col space-y-6" on:submit|preventDefault={submit}>
					<div class="mx-auto max-w-lg text-center">
						<h1 class="text-2xl font-bold sm:text-3xl">Iniciar Sesión</h1>
					</div>
					<Label class="space-y-2">
						<span>Correo electrónico</span>
						<Input type="email" name="email" placeholder="name@company.com" required />
					</Label>
					<Label class="space-y-2">
						<span>Contraseña</span>
						<Input type="password" name="password" placeholder="••••••••••" required />
					</Label>
					<div class="flex items-start">
						<a
							href="forgot_password"
							class="ml-auto text-sm text-blue-700 hover:underline dark:text-blue-500"
							>¿Olvidó su contraseña?</a
						>
					</div>
					<Button type="submit" class="w-full1">Iniciar Sesión</Button>
					<p class="text-sm font-light text-gray-500 dark:text-gray-400">
						¿No tienes cuenta? <a
							href="register"
							class="font-medium text-primary-600 hover:underline dark:text-primary-500"
							>Regístrese</a
						>
					</p>
				</form>
			</div>
		</Register>
	</div>
</section>
