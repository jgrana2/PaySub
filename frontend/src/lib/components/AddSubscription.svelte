<script lang="ts">
	import { Plus } from 'svelte-heros-v2';
	import { Button, Input, Label, Modal, Select, Textarea, Fileupload } from 'flowbite-svelte';
	import { saveSubscription, saveImageToBucket } from '$lib/appwrite';

	let defaultModal = false;
	let selectedFrequency: string;
	let opciones = [
		{ value: 'Cada hora', name: 'Cada hora' },
		{ value: 'Diaria', name: 'Diaria' },
		{ value: 'Semanal', name: 'Semanal' },
		{ value: 'Mensual', name: 'Mensual' },
		{ value: 'Anual', name: 'Anual' }
	];

	let imagePreviewUrl: string = '';

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
		const formData = new FormData(event.target);
		let data = {
			title: formData.get('title'),
			subtitle: formData.get('subtitle'),
			description: formData.get('description'),
			frequency: selectedFrequency,
			is_enabled: true,
			price: formData.get('price'),
			long_description: formData.get('long-description')
		};
		try {
			const fileInput = (event.target as HTMLFormElement).querySelector('input[type="file"]');
			if (fileInput && fileInput.files.length > 0) {
				const file = fileInput.files[0];

				// Save the file to the bucket
				const response = await saveImageToBucket(file);
				const image_file_id = response.$id;
				const image_bucket_id = response.bucketId;

				// Add image_file_id and image_bucket_id to the data object
				data = { ...data, image_file_id, image_bucket_id };
			}
			await saveSubscription(data);
			alert('Suscripción creada');
			defaultModal = false;
			imagePreviewUrl = ''; // Reset the image preview after submission
			window.location.reload();
		} catch (error) {
			console.log('Error creando la suscripción.');
		}
	}
</script>

<div class="absolute bottom-0 right-0 mb-4 mr-4 z-10">
	<Button
		on:click={() => (defaultModal = true)}
		class="w-16 h-16 rounded-full transition-all shadow hover:shadow-lg transform hover:scale-110 flex items-center justify-center"
	>
		<svelte:component this={Plus}></svelte:component>
	</Button>
</div>

<Modal title="Agregar Nueva Suscripción" bind:open={defaultModal} class="min-w-full">
	<form on:submit|preventDefault={handleSubmit}>
		<div class="grid gap-4 mb-4 sm:grid-cols-2">
			<div class="sm:col-span-2">
				<Label for="title" class="mb-2">Título de la suscripción</Label>
				<Input
					type="text"
					id="title"
					name="title"
					placeholder="Escriba el título de la suscripción"
					required
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
				/>
			</div>
			<div>
				<Label
					>Frecuencia de pago
					<Select class="mt-2" items={opciones} bind:value={selectedFrequency} required />
				</Label>
			</div>
			<div>
				<Label for="price" class="mb-2">Precio</Label>
				<Input type="text" id="price" placeholder="$29999" name="price" required />
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
				/>
			</div>
			<div class="sm:col-span-2">
				<Label for="description" class="mb-2">Descripción larga (compatible con Markdown)</Label>
				<Textarea
					id="long-description"
					placeholder="Describa la suscripción"
					rows="4"
					name="long-description"
				/>
			</div>
			<Button type="submit" class="w-52">Agregar suscripción</Button>
		</div>
	</form>
</Modal>
