<script lang="ts">
	import { PlusCircle, Trash } from 'svelte-heros-v2';
	import { getCards, deleteCard } from '$lib/appwrite';
	import { Spinner, Button, Modal } from 'flowbite-svelte';

	// Example array of newsletter cards
	let cards = [];
	let isLoading = true; // Initial state
	let defaultModal = false;

	export async function fetchCards() {
		try {
			cards = await getCards();
			for (const card of cards) {
				card.card_number = await decryptCardNumber(card.card_number);
			}
		} catch (error) {
			console.error('An error occurred:', error);
		} finally {
			isLoading = false;
		}
	}
	fetchCards();

	async function deleteCardRefresh(card: any) {
		await deleteCard(card);
		window.location.reload();
	}

	async function decryptCardNumber(card_number) {
		try {
			const response = await fetch(`https://api.paysub.app/decrypt`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					payload: card_number
				})
			});
			// Check if the response is okay (status code 200-299)
			if (!response.ok) {
				throw new Error(`Server responded with ${response.status}: ${await response.text()}`);
			}

			// Assuming the server sends back JSON data
			let responseData = await response.json();
			return responseData.decrypted_data;
		} catch (err) {
			// Log any errors to the console and capture them for display
			console.error('There was an issue with the encryption request:', err.message);
			let error = err.message;
		}
	}
</script>

{#if isLoading}
	<div class="flex justify-center h-[calc(100vh-300px)]">
		<Spinner />
	</div>
{:else if cards.length === 0}
	<div class="flex flex-col justify-center items-center h-[calc(100vh-300px)]">
		<img src="fondotabla.png" alt="No tienes suscriptores" class="w-40 mb-4 opacity-30" />
		<p class="text-center text-gray-700">
			No tienes tarjetas aún, presione
			<PlusCircle class="inline-block mx-2" />
			para agregar una nueva tarjeta
		</p>
	</div>
{:else}
	<div class="flex flex-col w-full rounded-lg border">
		<table class="table-auto w-full p-2 bg-slate-50 rounded-lg">
			<thead>
				<tr class="table-header">
					<th class="text-sm text-left">Número</th>
					<th class="text-sm text-left">Nombre</th>
					<th class="text-sm text-left">CVC</th>
					<th class="text-sm text-left">Expiración</th>
					<th class="text-sm text-left">No. ID</th>
					<th class="text-sm text-left">Eliminar</th>
				</tr>
			</thead>
			<tbody>
				{#each cards as card, index}
					<tr
						class={`table-row hover:bg-slate-100 ${index % 2 === 0 ? 'bg-white' : 'bg-slate-50'}`}
					>
						<!-- <td class="text-sm">•••• •••• •••• {card.card_number.slice(-4)}</td> -->
						<td class="text-sm">•••• •••• •••• {card.card_number.slice(-4)}</td>
						<td class="text-sm">{card.card_holder}</td>
						<td class="text-sm">•••{card.cvc.slice(-1)}</td>
						<td class="text-sm">{card.expiration}</td>
						<td class="text-sm">•••••••••{card.card_holder_id_number.slice(-3)}</td>
						<td class="text-sm">
							<button on:click={() => (defaultModal = true)}>
								<Trash size="20" />
							</button>
						</td>
					</tr>
					<Modal title="" bind:open={defaultModal} autoclose size="sm" class="w-full">
						<svg
							class="text-gray-400 dark:text-gray-500 w-11 h-11 mb-3.5 mx-auto"
							aria-hidden="true"
							fill="currentColor"
							viewBox="0 0 20 20"
							xmlns="http://www.w3.org/2000/svg"
							><path
								fill-rule="evenodd"
								d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
								clip-rule="evenodd"
							/></svg
						>
						<p class="mb-4 text-gray-500 dark:text-gray-300 text-center">
							¿Estás seguro de que quieres eliminar esta tarjeta?
						</p>
						<div class="flex justify-center items-center space-x-4">
							<Button color="light">No, cancelar</Button>
							<Button color="red" on:click={deleteCardRefresh(card)}>Si estoy seguro</Button>
						</div>
					</Modal>
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
