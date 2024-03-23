<script lang="ts">
	import { onMount } from 'svelte';
	import Header from '$lib/components/Header.svelte';
	import { Rating, Badge } from 'flowbite-svelte';
	import user from '../../store/user';
	import Reviews from '$lib/components/Reviews.svelte';

	/** @type {import('./$types').PageData} */
	export let data; // Subscription ID from url parameters

	let subscription = {}; // Create a writable store for the subscription data
	let loggedInUser = {}; // Initialize loggedInUser as an empty object
	let isLoggedIn = false;

	user.subscribe((user) => {
		loggedInUser = user;
		// Check if loggedInUser is not null and has properties (not an empty object)
		isLoggedIn = loggedInUser && Object.keys(loggedInUser).length > 0;
	});

	onMount(async () => {
		const response = await fetch(`https://api.paysub.app/subscription/${data.id}`);
		if (response.ok) {
			const jsonData = await response.json();
			subscription = jsonData;
		}
	});

	async function pay_subscription(e) {
		e.preventDefault();
		if (isLoggedIn) {
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

	// In your JavaScript file or script tag
	const tableRows = [
		{ isHeader: true, detail: 'Header 1', description: 'Description 1' },
		{ isHeader: false, detail: 'Data 1', description: 'Detail 1' },
		{ isHeader: false, detail: 'Data 2', description: 'Detail 2' }
		// ... more rows
	];
</script>

<Header></Header>

<!-- Main container -->
<div class="flex h-full items-center justify-center">
	<!-- Product container -->
	<div class="flex flex-col h-full max-w-5xl shadow-2xl sm:flex-row sm:h-fit p-4 gap-8">
		<!-- Main image -->
		<div class="w-full items-center justify-center flex">
			<img src="../bookcover.png" alt="Book cover" class="w-full" />
		</div>
		<!-- Product details -->
		<div class="flex flex-col w-full gap-4">
			<span class="text-xs">LIBRO</span>
			<span class="text-2xl font-mono"
				>Embedded Systems Engineering: Programs, Curriculum, and Emerging Trends</span
			>
			<div class="flex items-center gap-2">
				<Rating rating="4" size="24">
					<Badge slot="text" class="ms-3">4</Badge>
				</Rating>
				<span class="underline text-sm">8 reviews</span>
			</div>
			<span class="text-lg font-bold">Todo lo que querías saber sobre los sistemas embebidos</span>
			<span
				>"Embedded Systems Engineering: Programs, Curriculum, and Emerging Trends" is a
				comprehensive practical guide of the field of embedded systems engineering. It covers a
				range of topics emphasizing the importance of hardware and software integration, real-time
				systems, low-level programming, digital and analog circuit design, power management, and
				security considerations in embedded systems design and application.</span
			>
			<div class="flex">
				<table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
					<thead
						class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
					>
					</thead>
					<tbody>
						<tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
							<td class="">ASIN</td>
							<td class="">B0CV65NDJ6</td>
						</tr>
						<tr class="bg-gray-50 border-b dark:bg-gray-900 dark:border-gray-700">
							<td class="">Fecha de publicación</td>
							<td class="">6 Febrero 2024</td>
						</tr>
						<tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
							<td class="">Idioma</td>
							<td class="">Inglés</td>
						</tr>
						<tr class="bg-gray-50 border-b dark:bg-gray-900 dark:border-gray-700">
							<td class="">Tamaño del archivo</td>
							<td class="">1923 KB</td>
						</tr>
						<tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
							<td class="">Uso simultáneo de dispositivos</td>
							<td class="">Sin límite</td>
						</tr>
						<tr class="bg-gray-50 border-b dark:bg-gray-900 dark:border-gray-700">
							<td class="">Texto a voz</td>
							<td class="">Activado</td>
						</tr>
						<tr class="bg-gray-50 border-b dark:bg-gray-900 dark:border-gray-700">
							<td class="">Tipografía mejorada</td>
							<td class="">Activado</td>
						</tr>
						<tr class="bg-gray-50 dark:bg-gray-900">
							<td class="">Número de páginas</td>
							<td class="">159 páginas</td>
						</tr>
					</tbody>
				</table>
			</div>
			<div class="flex justify-between">
				<div class="flex gap-2 items-center">
					<input
						type="checkbox"
						class="before:content[''] peer relative h-5 w-5 cursor-pointer appearance-none rounded-md border border-blue-gray-200 transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-12 before:w-12 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-blue-gray-500 before:opacity-0 before:transition-opacity checked:border-gray-900 checked:bg-gray-900 checked:before:bg-gray-900 hover:before:opacity-10"
						id="checkbox"
						checked
					/><span>PDF</span>
					<input
						type="checkbox"
						class="before:content[''] peer relative h-5 w-5 cursor-pointer appearance-none rounded-md border border-blue-gray-200 transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-12 before:w-12 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-blue-gray-500 before:opacity-0 before:transition-opacity checked:border-gray-900 checked:bg-gray-900 checked:before:bg-gray-900 hover:before:opacity-10"
						id="checkbox"
						checked
					/><span>epub</span>
				</div>
				<span class="font-thin">$35</span>
			</div>
			<button class="border bg-orange-500 shadow p-2 text-white text-sm">COMPRAR</button>
		</div>
	</div>
</div>