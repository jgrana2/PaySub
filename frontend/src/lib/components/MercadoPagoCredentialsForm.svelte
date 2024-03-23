<script lang="ts">
	import { getAccessToken, saveAccessToken } from '$lib/appwrite';

	let accessToken = '';
	let tokenExists = false;

	async function check_token() {
		try {
			tokenExists = await getAccessToken();
		} catch (error) {
			console.error('Session check failed:', error);
		}
	}

	check_token();

	// Submit form handler
	async function submit(e: Event) {
		e.preventDefault();
		const form = e.target as HTMLFormElement;
		const formData = new FormData(form);
		const accessToken = formData.get('access-token') as string;
		let encryptedAccessToken = '';

		if (form.checkValidity()) {
			try {
				const response = await fetch(`https://api.paysub.app/encrypt`, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({
						payload: accessToken
					})
				});
				// Check if the response is okay (status code 200-299)
				if (!response.ok) {
					throw new Error(`Server responded with ${response.status}: ${await response.text()}`);
				}

				// Assuming the server sends back JSON data
				let responseData = await response.json();
				encryptedAccessToken = responseData.encrypted_data;
			} catch (err) {
				// Log any errors to the console and capture them for display
				console.error('There was an issue with the encryption request:', err.message);
				let error = err.message;
			}
			try {
				await saveAccessToken({ mp_access_token: encryptedAccessToken });
				alert(
					'Credencial guardada exitosamente \n¡Ya estás listo para hacer crecer tu negocio con PaySub!'
				);
				window.location.href = 'subscriptions';
			} catch (error) {
				alert('Error guardando la credencial: ' + error);
			}
		} else {
			// Handle the invalid form here
			console.log('The form is not valid.');
		}
	}

	function validateAccessToken(event: Event & { currentTarget: HTMLInputElement }) {
		const target = event.currentTarget;
		accessToken = target.value;
		if (
			!(accessToken.length >= 70 && accessToken.length <= 73) ||
			!(accessToken.startsWith('TEST-') || accessToken.startsWith('APP_USR-'))
		) {
			target.setCustomValidity('Access Token inválido');
		} else {
			target.setCustomValidity(''); // Clear custom validity message
		}
		target.reportValidity();
	}
</script>

<div class="flex flex-col">
	<span class="text-lg font-bold">Añade Tu Credencial de Mercado Pago</span>
	<span class="text-sm">¡Conecta tu cuenta y comienza a recibir pagos en un instante!</span>
	<span class="text-sm mb-4"
		>Sólo con agregar tu credencial de producción en esta sección, podrás iniciar la recepción de
		pagos directamente en tu billetera de Mercado Pago 🚀💳✨</span
	>
	<span class="font-bold">Instrucciones:</span>
	<ol class="list-decimal list-inside mb-4 text-sm">
		<li>
			<strong>Regístrate en Mercado Pago para Desarrolladores:</strong> Empieza por crear tu cuenta
			siguiendo las instrucciones disponibles
			<a
				href="https://www.mercadopago.com.co/hub/registration/splitter?contextual=normal&entity=pf&redirect_url=https://www.mercadopago.com.co/developers/es"
			>
				<span class="underline">aquí</span></a
			>
		</li>
		<li>
			<strong>Crea una aplicación para tu empresa o negocio:</strong> Crea una aplicación en el panel
			de desarrollador de Mercado Pago. Este es el primer paso para configurar tus integraciones.
		</li>
		<li>
			<strong>Credenciales de Producción:</strong> Accede a tu aplicación recien creada a través de "Tus
			integraciones" y en el menú izquierdo selecciona 'Credenciales de Producción'. Es aquí donde obtendrás
			el acceso necesario para operar.
		</li>
		<li>
			<strong>Obtén tu <span class="italic">Access Token:</span></strong> Copia el valor del Access Token
			y pégalo en el siguiente formulario para registrar tu credencial.
		</li>
	</ol>
	{#if tokenExists}
		<span class="mb-4 text-sm font-bold text-green-500"
			>Tu token ya está almacenado. Por motivos de seguridad, no podemos mostrarlo. Si deseas
			actualizarlo, usa el formulario proporcionado. Recuerda que esto reemplazará el token
			existente. Verifica que el nuevo token esté vinculado a tu cuenta de Mercado Pago y tu
			aplicación de integración.</span
		>
	{/if}
	<form class="w-full flex flex-col mb-4" on:submit|preventDefault={submit}>
		<div class="mb-5 w-full">
			<label for="access-token" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
				>Access Token:</label
			>
			<input
				type="password"
				id="access-token"
				name="access-token"
				class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light"
				required
				bind:value={accessToken}
				on:input={validateAccessToken}
			/>
		</div>
		<button
			type="submit"
			class="text-white w-fit bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
			>Agregar credencial</button
		>
	</form>
</div>
