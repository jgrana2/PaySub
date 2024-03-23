<script>
	import { ComputerDesktop, PencilSquare, PlusCircle } from 'svelte-heros-v2';
	import { Spinner, Toggle } from 'flowbite-svelte';
	import { onMount } from 'svelte';
	import user from '../../store/user';
	import { updateSubscriber } from '$lib/appwrite';

	let activeSubscriptions = [];
	let isLoading = true; // Initial state

	let loggedInUser = {}; // Initialize loggedInUser as an empty object
	user.subscribe((user) => {
		loggedInUser = user;
	});

	onMount(async () => {
		const response = await fetch(
			`https://api.paysub.app/active_subscriptions/${loggedInUser.email}`
		);
		if (response.ok) {
			const jsonData = await response.json();
			activeSubscriptions = jsonData;
			isLoading = false;
		}
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

	async function toggleSubscription(subscription) {
		if (subscription.is_active) {
			subscription.is_active = false;
			let data = {$id: subscription.$id, is_active: false}
			await updateSubscriber(data)
		}else {
			subscription.is_active = true;
			let data = {$id: subscription.$id, is_active: true}
			await updateSubscriber(data)
		}
		
	}
</script>

{#if isLoading}
	<div class="flex justify-center h-[calc(100vh-300px)]">
		<Spinner />
	</div>
{:else if activeSubscriptions.length === 0}
	<div class="flex flex-col justify-center items-center h-[calc(100vh-300px)]">
		<img src="fondotabla.png" alt="No tienes suscriptores" class="w-40 mb-4 opacity-30" />
		<p class="text-center text-gray-700">
			No cuentas con suscripciones activas. Al suscribirte, aparecerán listadas en esta sección
		</p>
	</div>
{:else}
	<div class="flex flex-col w-full rounded-lg border">
		<table class="table-auto w-full bg-slate-50 rounded-lg">
			<thead>
				<tr class="table-header">
					<th class="text-sm text-left">ID Suscripción</th>
                    <th class="text-sm text-left">Estado</th>
					<th class="text-sm text-left">Fecha de inicio</th>
					<th class="text-sm text-left">Próxima renovación</th>
					<th class="text-sm text-left">Activar</th>
				</tr>
			</thead>
			<tbody>
				{#each activeSubscriptions as subscription, index}
					<tr
						class={`table-row hover:bg-slate-100 ${index % 2 === 0 ? 'bg-white' : 'bg-slate-50'}`}
					>
						<td class="text-sm">{subscription.title}</td>
                        <td class="text-sm">{subscription.is_active ? 'Activa' : 'Inactiva'}</td>
						<td class="text-sm">{formatDate(subscription.subscription_start_date)}</td>
                        <td class="text-sm">{formatDate(subscription.renewal_date)}</td>
						<td class="text-sm flex">
							<Toggle checked={subscription.is_active} on:change={toggleSubscription(subscription)}></Toggle>
						</td>
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
