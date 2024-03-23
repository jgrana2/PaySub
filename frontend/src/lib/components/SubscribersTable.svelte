<script lang="ts">
	import { PencilSquare } from 'svelte-heros-v2';
	import { getSubscribers } from '$lib/appwrite';
	import { Spinner } from 'flowbite-svelte';
	import { onMount } from 'svelte';

	// Example array of newsletter subscribers
	let subscribers = [];
	let isLoading = true; // Initial state

	export async function fetchSubscribers() {
		try {
			subscribers = await getSubscribers();
		} catch (error) {
			console.error('An error occurred:', error);
		} finally {
			isLoading = false;
		}
	}

	onMount(() => {
		fetchSubscribers();
	});

	function formatDate(isoString) {
		// Check if the input string is actually a valid date.
		const date = new Date(isoString);
		if (isNaN(date)) {
			return 'Invalid Date';
		}

		// Use 'es-CO' as a default locale and set the timeZone to 'UTC'
		// to avoid inconsistencies across different time zones.
		return date.toLocaleDateString('es-CO', {
			year: 'numeric',
			month: 'long',
			day: 'numeric',
			hour: '2-digit',
			minute: '2-digit',
			timeZone: 'UTC' // Using UTC to avoid local timezone differences
		});
	}
</script>

{#if isLoading}
	<div class="flex justify-center h-[calc(100vh-300px)]">
		<Spinner />
	</div>
{:else if subscribers.length === 0}
	<div class="flex flex-col justify-center items-center h-[calc(100vh-300px)]">
		<img src="fondotabla.png" alt="No tienes suscriptores" class="w-40 mb-4 opacity-30" />
		<p class="text-center text-gray-700">
			No tienes suscriptores aún, crea una suscripción y compártela a tus clientes para que se
			suscriban
		</p>
	</div>
{:else}
	<div class="flex flex-col w-full rounded-lg border">
		<table class="table-auto w-full p-2 bg-slate-50 rounded-lg">
			<thead>
				<tr class="table-header">
					<th class="text-sm text-left">Email</th>
					<th class="text-sm text-left">Título de la suscripción</th>
					<th class="text-sm text-left">Fecha de inicio</th>
					<th class="text-sm text-left">Fecha de renovación</th>
					<th class="text-sm text-left">Estado</th>
				</tr>
			</thead>
			<tbody>
				{#each subscribers as subscriber, index}
					<tr
						class={`table-row hover:bg-slate-100 ${index % 2 === 0 ? 'bg-white' : 'bg-slate-50'}`}
					>
						<td class="text-sm">{subscriber.email}</td>
						<td class="text-sm">{subscriber.title}</td>
						<td class="text-sm">{formatDate(subscriber.subscription_start_date)}</td>
						<td class="text-sm">{formatDate(subscriber.renewal_date)}</td>
						<td class="text-sm">{subscriber.is_active ? 'Activa' : 'Inactiva'}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/if}

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
