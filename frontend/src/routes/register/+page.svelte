<script>
	import { register } from '$lib/appwrite';
	import { Button, Checkbox, Label, Input } from 'flowbite-svelte';

	let termsAccepted = false; // Track if terms and conditions are accepted.

	function submit(e) {
		e.preventDefault();
		const formData = new FormData(e.target);
		const firstname = formData.get('firstname');
		const lastname = formData.get('lastname');
		const phone = formData.get('phone');
		const email = formData.get('email');
		const password = formData.get('password');
		const confirmPassword = formData.get('confirm-password');

		if (!termsAccepted) {
			alert('Debe aceptar los términos y condiciones para continuar');
			return;
		}

		if (password !== confirmPassword) {
			alert('Las contraseñas deben coincidir');
			return;
		}

		// If `password` might be null, provide an empty string as a default.
		const safePassword = password || '';
		if (safePassword.length < 8) {
			alert('La contraseña debe tener al menos 8 caracteres');
			return;
		}

		register(firstname, lastname, phone, email, password);
	}

	function toggleTerms(checked) {
		termsAccepted = checked;
	}
</script>

<section class="relative flex flex-wrap lg:h-screen lg:items-center">
	<div class="relative h-64 w-full sm:h-96 lg:h-full lg:w-1/2">
		<img alt="Welcome" src="form_image.jpg" class="absolute inset-0 h-full w-full object-cover" />
	</div>
	<div class="w-full px-4 py-12 sm:px-6 sm:py-16 lg:w-1/2 lg:px-8 lg:py-24">
		<div class="mx-auto max-w-lg text-center">
			<h1 class="text-2xl font-bold sm:text-3xl">Registrarse</h1>
		</div>

		<form class="flex flex-col space-y-6" on:submit|preventDefault={submit}>
			<Label class="space-y-2">
				<span>Nombre</span>
				<Input type="text" name="firstname" placeholder="María José" required/>
			</Label>
			<Label class="space-y-2">
				<span>Apellido</span>
				<Input type="text" name="lastname" placeholder="Lopez Perez" required/>
			</Label>
			<Label class="space-y-2">
				<span>Número de celular</span>
				<Input type="number" name="phone" placeholder="300123456" required/>
			</Label>
			<Label class="space-y-2">
				<span>Correo electrónico</span>
				<Input type="email" name="email" placeholder="nombre@empresa.com" required />
			</Label>
			<Label class="space-y-2">
				<span>Contraseña</span>
				<Input type="password" name="password" placeholder="••••••••••" required />
			</Label>
			<Label class="space-y-2">
				<span>Confirme su contraseña</span>
				<Input type="password" name="confirm-password" placeholder="••••••••••" required />
			</Label>
			<div class="flex items-center">
				<Checkbox on:change={(e) => toggleTerms(e.target.checked)} required></Checkbox>
				<span class="mr-1">Acepto los</span>
				<a href="terms" class="font-medium text-primary-600 hover:underline dark:text-primary-500">
					Términos y condiciones
				</a>
			</div>
			<Button type="submit" class="w-full">Crear Cuenta</Button>
			<div class="text-sm font-medium text-gray-500 dark:text-gray-300">
				¿Ya tiene cuenta? <a
					href="login"
					class="font-medium text-primary-600 hover:underline dark:text-primary-500"
					>Inicie sesión aquí</a
				>
			</div>
		</form>
	</div>
</section>
