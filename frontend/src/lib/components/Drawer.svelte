<script>
	import Logo from './Logo.svelte';
	import { XMark } from 'svelte-heros-v2';

	export let subscriber;
	/**
	 * @type {() => void}
	 */
	export let onClose;

	function saveChanges() {
		// Logic to save changes to the subscriber
		onClose(); // Close the drawer after saving changes
	}

	let user = {
		nombre: '',
		email: '',
		suscripciones: '',
		estado: '',
		contribucion: '',
		actualizado: ''
	};

	// Function to handle form submission
	const handleSubmit = () => {
		// Implement the update logic here
		console.log('Updating user:', user);
		// You would typically make an API call here to update the user data
	};
</script>

<div class="drawer">
	<div class="flex justify-between items-center">
		<button on:click={onClose} class="flex-shrink-0">
			<svelte:component this={XMark} size="25" />
		</button>
		<div class="flex-grow flex justify-center">
			<Logo></Logo>
		</div>
		<div class="flex-shrink-0 w-8"><!-- Placeholder to balance the layout --></div>
	</div>

	<div class="flex flex-col p-4">
		<form on:submit|preventDefault={handleSubmit} class="space-y-6">
			<div class="flex flex-col">
				<label for="nombre" class="text-gray-700">Nombre:</label>
				<input
					type="text"
					id="nombre"
					bind:value={user.nombre}
					class="mt-1 p-2 border rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
				/>
			</div>

			<div class="flex flex-col">
				<label for="email" class="text-gray-700">Email:</label>
				<input
					type="email"
					id="email"
					bind:value={user.email}
					class="mt-1 p-2 border rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
				/>
			</div>

			<div class="flex flex-col">
				<label for="suscripciones" class="text-gray-700">Suscripciones:</label>
				<select
					id="suscripciones"
					bind:value={user.suscripciones}
					class="mt-1 p-2 border rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
				>
					<!-- Replace these options with your actual subscription options -->
					<option value="basic">Basic</option>
					<option value="standard">Standard</option>
					<option value="premium">Premium</option>
				</select>
			</div>

			<div class="flex flex-col">
				<label for="estado" class="text-gray-700">Estado:</label>
				<select
					id="estado"
					bind:value={user.estado}
					class="mt-1 p-2 border rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
				>
					<option value="">Seleccione un estado</option>
					<option value="activo">Activo</option>
					<option value="inactivo">Inactivo</option>
				</select>
			</div>

			<div class="flex flex-col">
				<label for="contribucion" class="text-gray-700">Contribución:</label>
				<input
					type="number"
					id="contribucion"
					bind:value={user.contribucion}
					class="mt-1 p-2 border rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
				/>
			</div>

			<div class="flex flex-col">
				<label for="actualizado" class="text-gray-700">Actualizado:</label>
				<input
					type="date"
					id="actualizado"
					bind:value={user.actualizado}
					class="mt-1 p-2 border rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
				/>
			</div>

			<button
				type="submit"
				class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
			>
				Editar
			</button>
		</form>
	</div>
</div>

<style>
	.drawer {
		/* Styles for your drawer */
		position: fixed;
		right: 0;
		top: 0;
		width: 300px; /* Adjust as needed */
		height: 100%;
		background-color: white;
		box-shadow: -2px 0 5px rgba(225, 225, 225, 0.2);
		z-index: 1000;
		/* More styles for animation and layout */
	}
</style>
