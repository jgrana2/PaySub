<script lang="ts">
	import { onMount } from 'svelte';
	import Header from '$lib/components/Header.svelte';
	import { Rating, Badge, Tooltip, Spinner } from 'flowbite-svelte';
	import user from '../../../store/user';
	import { getImage } from '$lib/appwrite';
	import SvelteMarkdown from 'svelte-markdown';
	import { ImagePlaceholder, Button } from 'flowbite-svelte';

	/** @type {import('./$types').PageData} */
	export let data; // Subscription ID from url parameters

	let subscription = {}; // Create a writable store for the subscription data
	let loggedInUser = {}; // Initialize loggedInUser as an empty object
	let isLoggedIn = false;
	let image_url = null;
	let renew_date = null;
	let status = null;
	let isLoading = true; // Initial state
	let isButtonClicked = false;
	let isProcessing = false;
	let isAlreadySubscribed = false;

	// WARNING: CRITICAL SECTION
	user.subscribe(async ($user) => {
		loggedInUser = $user;
		// Check if loggedInUser is not null and has properties (not an empty object)
		isLoggedIn = loggedInUser && Object.keys(loggedInUser).length > 0;
		const response = await fetch(
			`https://api.paysub.app/active_subscriptions/${loggedInUser.email}`
		);
		if (response.ok) {
			const jsonData = await response.json();
			let activeSubscriptions = jsonData;
			activeSubscriptions.forEach((subscriptionItem) => {
				// Fixing string comparison by ensuring both IDs are strings before comparing
				if (String(subscriptionItem.subscription_id) === String(data.id)) {
					if (subscriptionItem.is_active) {
						// The user is already subscribed
						isAlreadySubscribed = true;
						console.log('Already subscribed');
					}
				}
			});
		}
	});

	onMount(async () => {
		const response = await fetch(`https://api.paysub.app/subscription/${data.id}`);
		if (response.ok) {
			const jsonData = await response.json();
			subscription = jsonData;
			image_url = await getImage(subscription.image_file_id);
			renew_date = getNextCycleDate(subscription.frequency);
			if (subscription.is_enabled) {
				status = 'Activa';
			} else {
				status = 'Inactiva';
			}
		}
		isLoading = false;
	});

	function getNextCycleDate(frequency) {
		const currentDate = new Date();
		switch (frequency) {
			case 'hourly':
			case 'Cada hora':
				currentDate.setHours(currentDate.getHours() + 1);
				break;
			case 'daily':
			case 'Diaria':
				currentDate.setDate(currentDate.getDate() + 1);
				break;
			case 'weekly':
			case 'Semanal':
				currentDate.setDate(currentDate.getDate() + 7);
				break;
			case 'monthly':
			case 'Mensual':
				currentDate.setMonth(currentDate.getMonth() + 1);
				break;
			case 'yearly':
			case 'Anual':
				currentDate.setFullYear(currentDate.getFullYear() + 1);
				break;
			default:
				throw new Error('Invalid frequency');
		}
		// Formatting Date in the format of "Month day, year", with Spanish month names
		const monthNames = [
			'enero',
			'febrero',
			'marzo',
			'abril',
			'mayo',
			'junio',
			'julio',
			'agosto',
			'septiembre',
			'octubre',
			'noviembre',
			'diciembre'
		];

		const day = currentDate.getDate();
		const monthIndex = currentDate.getMonth();
		const year = currentDate.getFullYear();

		// Capitalizing the first letter of the month for proper formatting
		const monthNameCapitalized =
			monthNames[monthIndex].charAt(0).toUpperCase() + monthNames[monthIndex].slice(1);

		return `${monthNameCapitalized} ${day}, ${year}`; // Example: "Marzo 1, 2024"
	}

	async function pay_subscription(e) {
		if (!subscription.is_enabled) {
			alert('La subscripción está inactiva');
			return; // Stop execution if the subscription is disabled, this is also checked in the backend
		}
		if (isAlreadySubscribed) {
			alert('Ya está suscrito a esta suscripción');
			return; // Stop execution if already subscribed
		}
		if (isLoggedIn) {
			isButtonClicked = true;
			isProcessing = true;
			e.preventDefault();
			console.log('Procesando...');
			try {
				const hasCards = await userHasCards(loggedInUser.$id);
				if (hasCards.hasCards == 'false') {
					// Redireccionar para agregar método de pago
					window.location.href = `../../payment_method/${data.id}`;
				} else {
					try {
						const response = await fetch('https://api.paysub.app/activate-subscription', {
							method: 'POST',
							headers: {
								'Content-Type': 'application/json'
							},
							body: JSON.stringify({
								subscription_id: subscription.id,
								user_email: loggedInUser.email
							})
						});

						if (!response.ok) {
							if (!subscription.is_enabled) {
								alert('Error al suscribirse. La suscripción se encuentra inactiva.');
							} else {
								alert('Error al suscribirse. Falló el pago.');
							}
							isProcessing = false;
							isButtonClicked = false;
							throw new Error(`HTTP error! status: ${response.status}`);
						}

						// At this point, the payment is successful
						const data = await response.json();
						console.log(data);
						window.location.href = '../success';
					} catch (error) {
						console.error('There was an error activating the subscription:', error);
					}
				}
			} catch (error) {
				console.error('There was an error retrieving your cards:', error);
				alert('There was an error processing your payment method. Please try again later.');
				return; // Early return on error
			}
		} else {
			alert('Por favor inicie sesión para suscribirse.');
			window.location.href = `../login/${data.id}`;
		}
	}

	async function userHasCards(userId) {
		// Placeholder for actual implementation to get user cards
		// This will vary depending on your backend API and database
		// Replace with the actual API endpoint and logic to retrieve user's cards
		const response = await fetch(`https://api.paysub.app/cards?user_id=${userId}`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json'
			}
		});

		if (!response.ok) {
			throw new Error(`HTTP error while fetching cards! status: ${response.status}`);
		}

		return await response.json();
	}
</script>

<Header></Header>

<div class="flex flex-col items-center justify-center h-full max-w-screen-xl mx-auto mb-10">
	{#if isLoading}
		<ImagePlaceholder class="w-full" />
	{:else}
		<div class="group relative flex w-full h-full overflow-hidden">
			<div class="flex flex-col sm:flex-row h-full">
				<!-- Image -->
				<div class="w-full h-full">
					<button
						class="absolute start-4 top-4 z-10 rounded-full bg-white p-1.5 text-gray-900 transition hover:text-gray-900/75"
					>
						<span class="sr-only">Wishlist</span>

						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="1.5"
							stroke="currentColor"
							class="h-4 w-4"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"
							/>
						</svg>
					</button>

					<img
						src={image_url}
						alt=""
						class="h-full w-full object-cover transition duration-500 group-hover:scale-105"
					/>
				</div>

				<!-- Details panel -->
				<div class="relative bg-white sm:p-20 p-4 w-full flex flex-col text-justify">
					<span class="text-xs">SUSCRIPCIÓN</span>
					<span class="text-lg font-bold font-serif text-gray-900">{subscription.title}</span>
					<span class="text-sm font-bold font-serif text-gray-900 mb-4"
						>{subscription.subtitle}</span
					>
					<Rating rating="4" size="24" class="mb-5">
						<Badge slot="text" class="ms-3">4</Badge>
					</Rating>
					<div class="flex justify-between items-center text-xs items-stretch mb-4">
						<div class="sm:inline-flex sm:shrink-0 sm:items-center sm:gap-2">
							<svg
								class="h-4 w-4 text-indigo-700"
								xmlns="http://www.w3.org/2000/svg"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"
								/>
							</svg>

							<div class="mt-1.5 sm:mt-0">
								<p class="text-gray-500">Frecuencia</p>

								<p class="font-medium capitalize">{subscription.frequency}</p>
							</div>
							<Tooltip>Frecuencia de renovación de suscripción</Tooltip>
						</div>

						<div class="sm:inline-flex sm:shrink-0 sm:items-center sm:gap-2">
							<svg
								class="h-4 w-4 text-indigo-700"
								xmlns="http://www.w3.org/2000/svg"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"
								/>
							</svg>

							<div class="mt-1.5 sm:mt-0">
								<p class="text-gray-500">Próxima Renovación</p>
								<p class="font-medium">{renew_date}</p>
							</div>
							<Tooltip>Fecha de renovación de la suscripción</Tooltip>
						</div>

						<div class="sm:inline-flex sm:shrink-0 sm:items-center sm:gap-2">
							<svg
								class="h-4 w-4 text-indigo-700"
								xmlns="http://www.w3.org/2000/svg"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
								/>
							</svg>

							<div class="mt-1.5 sm:mt-0">
								<p class="text-gray-500">Estado</p>
								<p class="font-medium">{status}</p>
							</div>
							<Tooltip
								>Estado de la Suscripción<br />
								Activa: La suscripción está actualmente activa y se puede adquirir.<br />
								Inactiva: La suscripción no está disponible para la compra en este momento.
							</Tooltip>
						</div>
					</div>

					<SvelteMarkdown source={subscription.description}></SvelteMarkdown>
					<p class="mt-1.5 text-sm text-gray-700">${subscription.price}</p>

					<form class="mt-4" on:submit|preventDefault={pay_subscription}>
						<Button
							class="block w-full rounded p-4 text-sm font-medium transition hover:scale-105 text-center"
							on:click={pay_subscription}
							disabled={isButtonClicked}
						>
							{#if isProcessing}
								<Spinner class="me-3" size="4" />Procesando...
							{:else}
								Suscribirse
							{/if}
						</Button>
					</form>
				</div>
			</div>
		</div>
	{/if}
	{#if subscription.long_description}
		<div class="flex flex-col sm:flex-row max-w-screen-md sm:mt-20 text-justify list-outside p-4 sm:p-10">
			<div class="font-serif uppercase h-fit mr-20">Descripción</div>
			<div class="flex flex-col space-y-4">
				<SvelteMarkdown source={subscription.long_description}></SvelteMarkdown>
			</div>
		</div>
	{/if}
</div>
