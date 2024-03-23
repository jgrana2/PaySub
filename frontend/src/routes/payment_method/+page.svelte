<script lang="ts">
	import Header from '$lib/components/Header.svelte';
	import { LockClosed } from 'svelte-heros-v2';
	import valid from 'card-validator';
	import { onMount } from 'svelte';
	import { saveCard } from '$lib/appwrite';
	import user from '../../store/user';
	import { Spinner } from 'flowbite-svelte';

	let creditCardNumber = ''; // Initialize a reactive variable to store the credit card number
	let expiration = ''; // Initialize a reactive variable to store the expiration date
	let creditCardElement: HTMLInputElement; // Reference to store the input element for the card number
	let cardType = '';
	let cardTypeName = '';
	let loggedInUser = {}; // Initialize loggedInUser as an empty object
	let isLoggedIn = false;
	let supported = false;
	let isProcessing = false;

	user.subscribe((user) => {
		loggedInUser = user;
		// Check if loggedInUser is not null and has properties (not an empty object)
		isLoggedIn = loggedInUser && Object.keys(loggedInUser).length > 0;
	});

	onMount(async () => {
		validateCard(creditCardNumber); // Optional: Validate immediately on mount if pre-filled
	});

	function validateCardNumber(event: Event) {
		const target = event.target as HTMLInputElement;
		creditCardNumber = target.value;
		if (validateCard(creditCardNumber)) {
			target.setCustomValidity('');
		} else {
			target.setCustomValidity('Invalid card number.');
		}
		target.reportValidity();
	}

	async function handleSubmit(event: SubmitEvent & { currentTarget: HTMLFormElement }) {
		event.preventDefault();
		if (!supported) {
			alert('Tarjeta no soportada por el momento');
			return;
		}
		isProcessing = true;
		const formData = new FormData(event.currentTarget);

		if (validateCard(formData.get('card_number')) && isValidCVC(formData.get('cvc'))) {
			// Guardar tarjeta en base de datos
			const card_data = {
				card_number: formData.get('card_number').replace(/\s/g, ''), // Remove empty spaces
				card_holder: formData.get('card_holder'),
				card_holder_id_number: formData.get('document_id'),
				card_holder_id_type: formData.get('id_type'),
				expiration: formData.get('expiration'),
				cvc: formData.get('cvc'),
				card_payment_method_id: cardType,
				email: formData.get('email')
			};
			try {
				const response = await fetch(`https://api.paysub.app/encrypt`, {
					method: 'POST',
							headers: {
								'Content-Type': 'application/json'
							},
							body: JSON.stringify({
								payload: card_data.card_number
							})
						});
				// Check if the response is okay (status code 200-299)
				if (!response.ok) {
					throw new Error(`Server responded with ${response.status}: ${await response.text()}`);
				}

				// Assuming the server sends back JSON data
				let responseData = await response.json();
				card_data.card_number = responseData.encrypted_data;
			} catch (err) {
				// Log any errors to the console and capture them for display
				console.error('There was an issue with the encryption request:', err.message);
				let error = err.message;
			}
			try {
				await saveCard(card_data);
				alert('Tarjeta guardada exitósamente');
				window.location.href = 'cards';
			} catch (error) {
				isProcessing = false;
				alert('Error guardando la tarjeta');
			}
		}
	}

	function validateCard(cardNumber: string): boolean {
		const numberValidation = valid.number(cardNumber);

		if (numberValidation.card) {
			cardType = numberValidation.card.type; // Log card type such as 'visa'

			// Translate the value to mercadopago's accepted payment method IDs
			switch (numberValidation.card.type) {
				case 'american-express':
					cardType = 'amex';
					cardTypeName = 'American Express';
					supported = true;
					break;
				case 'mastercard':
					cardType = 'master';
					cardTypeName = 'Mastercard';
					supported = true;
					break;
				case 'visa':
					cardType = 'visa';
					cardTypeName = 'Visa';
					supported = true;
					break;
				case 'diners-club':
					cardType = 'diners';
					cardTypeName = 'Diners Club';
					supported = true;
					break;
				default:
					cardType = 'No compatible';
					cardTypeName = cardType;
					supported = false;
					break;
			}
		}

		if (!numberValidation.isPotentiallyValid || !numberValidation.isValid) {
			return false; // Return false to indicate the card is not valid.
		}
		return true; // The card is valid, so return true.
	}

	// This function handles the input and automatically inserts a slash when needed
	function formatExpirationInput(event) {
		let target = event.target;
		let value = target.value;

		// Remove all non-digit characters
		let cleanValue = value.replace(/\D+/g, '');

		// Extract potential month and year parts
		let monthPart = cleanValue.substring(0, 2);
		let yearPart = cleanValue.substring(2);

		// Parse the month and year to see if they're valid numbers
		let monthNumber = parseInt(monthPart, 10);
		let currentYear = new Date().getFullYear();
		let shortYear = currentYear % 100; // Get last two digits of current year for comparison
		let enteredYear = parseInt(yearPart, 10);

		// Initialize validity flag
		let isValid = true;

		// Check if the month is valid (1-12)
		if (monthNumber < 1 || monthNumber > 12) {
			target.setCustomValidity('Mes no válido. Por favor introduzca un valor entre 01 y 12.');
			isValid = false; // Month is not valid
		} else if (enteredYear < shortYear || enteredYear > shortYear + 10) {
			// Here we check if the year is in the past or too far in the future; adjust the range as needed
			target.setCustomValidity(
				`Año no válido. Por favor ingrese un valor entre ${shortYear} y ${shortYear + 10}.`
			);
			isValid = false; // Year is not valid
		} else {
			// If both month and year are valid, clear any custom validity messages
			target.setCustomValidity('');
		}

		target.reportValidity();

		// Automatically add slash if length is 2 and previous length was less than 2
		if (cleanValue.length === 2 && value.length < 5) {
			target.value = `${cleanValue}/`;
		} else if (cleanValue.length <= 4) {
			// Reformat the string in MM/YY format if it has 3 or 4 digits
			target.value = `${monthPart}${yearPart.length > 0 ? '/' + yearPart : ''}`;
		}

		// Update the reactive variable after formatting
		expiration = target.value;

		return isValid; // Return the validity of the expiration date
	}

	function validateCVCInput(event) {
		const inputElement = event.target;
		const cvc = inputElement.value;

		// First, clear any old validity messages
		inputElement.setCustomValidity('');

		// Extracted validation to a separate function
		if (!isValidCVC(cvc)) {
			const digitsRequired = cardType === 'amex' ? 4 : 3;
			inputElement.setCustomValidity(`El CVC debe tener una longitud de ${digitsRequired} dígitos`);

			// Report to the containing form that the input might be invalid
			inputElement.reportValidity();

			return false; // The CVC doesn't match
		} else {
			// Clear any custom validity message that may have been set
			inputElement.setCustomValidity('');

			// Always call reportValidity() to ensure the element displays any changes to its validation state
			inputElement.reportValidity();

			return true; // The CVC matches
		}
	}

	// New function to validate the CVC code
	function isValidCVC(cvc) {
		const cvcPattern = cardType === 'amex' ? /^\d{4}$/ : /^\d{3}$/;
		return cvcPattern.test(cvc);
	}
</script>

<Header></Header>

<div class="flex flex-col max-w-screen-sm mx-auto">
	<div class="text-lg font-bold pb-4 w-full px-4">Agregar Método de Pago</div>
	<form on:submit|preventDefault={handleSubmit} class="w-full p-4">
		<div class="flex justify-between">
			<div class="text-sm py-2">Número de tarjeta</div>
			<span class="inline-flex items-center rounded-md px-2 py-1 text-xs font-medium text-gray-600"
				>{cardTypeName}</span
			>
		</div>
		<div class="flex flex-col sm:flex-row items-center border-b mb-4 border-gray-500">
			<input
				bind:this={creditCardElement}
				class="appearance-none bg-transparent border-none w-full sm:w-2/4 text-gray-700 mb-4 sm:mb-0 sm:mr-3 py-1 px-2 leading-tight focus:outline-none"
				type="tel"
				placeholder="1234 5678 9012 3456"
				inputmode="numeric"
				name="card_number"
				bind:value={creditCardNumber}
				on:input={validateCardNumber}
				required
			/>
			<input
				class="appearance-none bg-transparent border-none w-full sm:w-1/4 text-gray-700 mb-4 sm:mb-0 sm:mr-3 py-1 px-2 leading-tight focus:outline-none"
				type="text"
				placeholder="MM/AA"
				name="expiration"
				bind:value={expiration}
				on:input={formatExpirationInput}
				maxlength="5"
				required
			/>
			<input
				class="appearance-none bg-transparent border-none w-full sm:w-1/4 text-gray-700 mb-4 sm:mb-0 sm:mr-3 py-1 px-2 leading-tight focus:outline-none"
				type="text"
				placeholder="CVC"
				maxlength="4"
				pattern="\d*"
				name="cvc"
				on:input={validateCVCInput}
				required
			/>
		</div>
		<div class="text-sm py-2">Nombre del titular</div>
		<div class="flex items-center border-b mb-4 border-gray-500">
			<input
				class="appearance-none bg-transparent border-none w-full text-gray-700 mb-4 sm:mb-0 sm:mr-3 py-1 px-2 leading-tight focus:outline-none"
				type="text"
				placeholder="María Lopez"
				name="card_holder"
				required
			/>
		</div>
		<div class="flex flex-col">
			<div class="text-sm py-2">Tipo de documento</div>
			<div class="flex items-center gap-2 text-xs mb-4">
				<input type="radio" name="id_type" value="CC" />Cédula de Ciudadanía
				<input type="radio" name="id_type" value="NIT" />NIT
			</div>
			<div class="text-sm py-2">Documento del titular</div>
			<div class="flex items-center border-b mb-4 border-gray-500">
				<input
					class="appearance-none bg-transparent border-none w-full text-gray-700 mb-4 sm:mb-0 sm:mr-3 py-1 px-2 leading-tight focus:outline-none"
					type="number"
					placeholder="123456789"
					name="document_id"
					required
				/>
			</div>
		</div>
		<div class="text-sm py-2">E-mail</div>
		<div class="flex items-center border-b mb-4 border-gray-500">
			<input
				class="appearance-none bg-transparent border-none w-full text-gray-700 mb-4 sm:mb-0 sm:mr-3 py-1 px-2 leading-tight focus:outline-none"
				type="email"
				placeholder="marialopez@ejemplo.com"
				name="email"
				required
			/>
		</div>
		<button
			type="submit"
			disabled={isProcessing}
			class="w-full justify-center bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center"
		>
			{#if isProcessing}
				<Spinner class="me-3" size="4" />Guardando tarjeta...
			{:else}
				<svelte:component this={LockClosed} size="15" class="flex-shrink-0 mr-2" />
				<span>Guardar tarjeta</span>
			{/if}
		</button>
	</form>
</div>
