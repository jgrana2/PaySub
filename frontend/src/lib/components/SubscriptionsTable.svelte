<script lang="ts">
	import { getImage, getSubscriptions, saveImageToBucket, updateSubscription } from '$lib/appwrite';
	import { ComputerDesktop, PencilSquare, PlusCircle } from 'svelte-heros-v2';
	import { Button, Input, Label, Modal, Select, Spinner, Textarea, Toggle } from 'flowbite-svelte';

	let subscriptions = [];
	let isLoading = true; // Initial state
	let isOpen = false;
	let editedSubscription = null;
	let imagePreviewUrl = '';
	let originalImageUrl = '';
	let selectedFrequency: string;

	// Translation mapping
	const frequencyOptions = {
		hourly: 'Cada hora',
		daily: 'Diaria',
		weekly: 'Semanal',
		monthly: 'Mensual',
		yearly: 'Anual'
	};

	let opciones = [
		{ value: 'Cada hora', name: 'Cada hora' },
		{ value: 'Diaria', name: 'Diaria' },
		{ value: 'Semanal', name: 'Semanal' },
		{ value: 'Mensual', name: 'Mensual' },
		{ value: 'Anual', name: 'Anual' }
	];

	export async function fetchSubscriptions() {
		try {
			const response = await getSubscriptions();
			// Process and map the response here
			subscriptions = response.map((sub) => ({
				...sub,
				description: truncateDescription(sub.description),
				frequency: translateFrequency(sub.frequency) // Translate the frequency here
			}));
		} catch (error) {
			console.error('An error occurred:', error);
		} finally {
			isLoading = false;
		}
	}

	// Function to truncate the description to 100 characters
	function truncateDescription(description) {
		return description.length > 100 ? `${description.slice(0, 100)}...` : description;
	}

	// Function to translate frequency to Spanish
	function translateFrequency(frequency) {
		return frequencyOptions[frequency] || frequency;
	}

	async function openModal(subscription) {
		imagePreviewUrl = ''; // Reset the image preview before submission
		isOpen = true;
		editedSubscription = {
			$id: subscription.$id,
			title: subscription.title,
			subtitle: subscription.subtitle,
			frequency: subscription.frequency,
			price: subscription.price,
			description: subscription.description,
			long_description: subscription.long_description,
			image_bucket_id: subscription.image_bucket_id,
			image_file_id: subscription.image_file_id,
			is_enabled: subscription.is_enabled
			};
		let image = await getImage(subscription.image_file_id);
		originalImageUrl = image.href; // Assuming 'href' is the property that holds the full image URL.
		imagePreviewUrl = originalImageUrl;
		console.log(editedSubscription);
	}

	function handleFileChange(event: Event) {
		const input = event.target as HTMLInputElement;
		if (input.files && input.files[0]) {
			const reader = new FileReader();
			reader.onload = (e: ProgressEvent<FileReader>) => {
				imagePreviewUrl = e.target.result.toString();
			};
			reader.readAsDataURL(input.files[0]); // Read the file as a data URL
		}
	}

	// Function to handle the creation of a new subscription
	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault(); // Prevent the form from reloading the page
		try {
			if (imagePreviewUrl !== originalImageUrl) {
				// The imagePreviewUrl has been updated
				console.log('Image has been updated');
				try {
					const fileInput = (event.target as HTMLFormElement).querySelector('input[type="file"]');
					if (fileInput && fileInput.files.length > 0) {
						const file = fileInput.files[0];

						// Save the file to the bucket
						const response = await saveImageToBucket(file);
						const image_file_id = response.$id;
						const image_bucket_id = response.bucketId;

						// Add image_file_id and image_bucket_id to the data object
						editedSubscription.image_file_id = image_file_id;
						editedSubscription.image_bucket_id = image_bucket_id;
					}
				} catch (error) {
					console.log('Error actualizando imagen');
				}
			}
			await updateSubscription(editedSubscription);
			alert('Suscripción actualizada');
			isOpen = false;
			imagePreviewUrl = ''; // Reset the image preview after submission
			window.location.reload();
		} catch (error) {
			console.log('Error creando la suscripción.');
		}
	}

	function handleToggleChange() {
		if (editedSubscription.is_enabled) {
			editedSubscription.is_enabled = false;
		} else {
			editedSubscription.is_enabled = true;
		}
		console.log('The toggle state is now:', editedSubscription.is_enabled);
	}

	fetchSubscriptions();
</script>

{#if isLoading}
	<div class="flex justify-center h-[calc(100vh-300px)]">
		<Spinner />
	</div>
{:else if subscriptions.length === 0}
	<div class="flex flex-col justify-center items-center h-[calc(100vh-300px)]">
		<img src="fondotabla.png" alt="No tienes suscriptores" class="w-40 mb-4 opacity-30" />
		<p class="text-center text-gray-700">
			No tienes suscripciones disponibles, presione
			<PlusCircle class="inline-block mx-2" />
			para agregar una nueva suscripción
		</p>
	</div>
{:else}
	<div class="flex flex-col w-full rounded-lg border">
		<table class="table-auto w-full bg-slate-50 rounded-lg">
			<thead>
				<tr class="table-header">
					<th class="text-sm text-left">Suscripción</th>
					<th class="text-sm text-left">Precio</th>
					<th class="text-sm text-left">Frecuencia</th>
					<th class="text-sm text-left">Descripción</th>
					<th class="text-sm text-left">Estado</th>
					<th class="text-sm text-left">Suscriptores</th>
					<th class="text-sm text-left">Ingresos</th>
					<th class="text-sm text-left">Editar</th>
				</tr>
			</thead>
			<tbody>
				{#each subscriptions as subscription, index}
					<tr
						class={`table-row hover:bg-slate-100 ${index % 2 === 0 ? 'bg-white' : 'bg-slate-50'}`}
					>
						<td class="text-sm">{subscription.title}</td>
						<td class="text-sm">${(subscription.price / 1000).toFixed(3)}</td>
						<td class="text-sm capitalize">{subscription.frequency}</td>
						<td class="text-sm">{subscription.description}</td>
						<td class="text-sm">{subscription.is_enabled ? 'Activa' : 'Inactiva'}</td>
						<td class="text-sm">{subscription.n_subscribers}</td>
						<td class="text-sm">${(subscription.income / 1000).toFixed(3)}</td>
						<td class="text-sm flex">
							<button class="flex" on:click={openModal(subscription)}>
								<svelte:component this={PencilSquare} size="20" />
							</button>
							<a href="subscription/{subscription.$id}" class="flex">
								<svelte:component this={ComputerDesktop} size="20" />
							</a>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/if}

<Modal title="Editar Suscripción" bind:open={isOpen} class="min-w-full">
	<form on:submit|preventDefault={handleSubmit}>
		<div class="grid gap-4 mb-4 sm:grid-cols-2">
			<div>
				<Toggle checked={editedSubscription.is_enabled} on:change={handleToggleChange}>Activar</Toggle>
			</div>
			<div class="sm:col-span-2">
				<Label for="title" class="mb-2">Título de la suscripción</Label>
				<Input
					type="text"
					id="title"
					name="title"
					placeholder="Escriba el título de la suscripción"
					required
					bind:value={editedSubscription.title}
				/>
			</div>
			<div class="sm:col-span-2">
				<Label for="subtitle" class="mb-2">Subtítulo de la suscripción</Label>
				<Input
					type="text"
					id="subtitle"
					name="subtitle"
					placeholder="Subtítulo de la suscripción"
					required
					bind:value={editedSubscription.subtitle}
				/>
			</div>
			<div>
				<Label
					>Frecuencia de pago
					<Select
						class="mt-2"
						items={opciones}
						bind:value={editedSubscription.frequency}
						required
					/>
				</Label>
			</div>
			<div>
				<Label for="price" class="mb-2">Precio</Label>
				<Input
					type="text"
					id="price"
					placeholder="$29999"
					name="price"
					required
					bind:value={editedSubscription.price}
				/>
			</div>
			<div>
				<Label class="space-y-2 mb-2">
					<span>Subir imagen</span>
					<input type="file" accept="image/*" on:change={handleFileChange} />
					{#if imagePreviewUrl}
						<img src={imagePreviewUrl} alt="Image preview" style="max-width: 200px;" />
					{/if}
				</Label>
				
			</div>
			<div class="sm:col-span-2">
				<Label for="description" class="mb-2">Descripción</Label>
				<Textarea
					id="description"
					placeholder="Describa la suscripción"
					rows="4"
					name="description"
					required
					bind:value={editedSubscription.description}
				/>
			</div>
			<div class="sm:col-span-2">
				<Label for="description" class="mb-2">Descripción larga (compatible con Markdown)</Label>
				<Textarea
					id="long-description"
					placeholder="Describa la suscripción"
					rows="4"
					name="long-description"
					bind:value={editedSubscription.long_description}
				/>
			</div>
			<Button type="submit" class="w-52">Actualizar Suscripción</Button>
		</div>
	</form>
</Modal>

<style>
	.table-header th {
		padding: 0.5rem;
		border-bottom: 1px solid #ddd;
	}

	.table-row td {
		padding: 0.5rem;
		border-bottom: 1px solid #eee;
	}
</style>
