<script lang="ts">
	import { Avatar, Dropdown, DropdownDivider, DropdownHeader, DropdownItem } from 'flowbite-svelte';
	import user from '../../store/user';
	import { handleLogout } from '../../store/user';
	const avatarStatusColor = 'green';
	const manageSubscriptionsLink = 'subscriptions';
	const manageCardsLink = 'cards';
	const manageSubscribersLink = 'subscribers';
	const managePaymentProcessingLink = 'payment_processing';

	export let title: string;
	let loggedInUser = {}; // Initialize loggedInUser as an empty object

	user.subscribe((user) => {
		loggedInUser = user;
	});
</script>

<!-- Container for the header section with flexbox layout -->
<div class="flex justify-between items-center h-14 w-full flex-shrink-0 px-4 text-gray-500 dark:text-gray-400">
	<!-- Title of the page/subsection -->
	<h3 class="text-2xl font-bold">{title}</h3>

	<!-- User avatar with a green dot indicating availability/status -->
	<Avatar
		id="user-drop"
		class="cursor-pointer"
		alt={`Avatar de ${loggedInUser.name}`}
		dot={{ color: avatarStatusColor }}
	/>

	<!-- Dropdown menu triggered by clicking on the user avatar -->
	<Dropdown triggeredBy="#user-drop" class="text-gray-500 dark:text-gray-400">
		<!-- Header section of the dropdown showing user information -->
		<DropdownHeader>
			<span class="block text-sm font-bold text-gray-500 dark:text-gray-400">{loggedInUser.name}</span>
			<!-- User's name -->
			<span class="block truncate text-xs  text-gray-500 dark:text-gray-400">{loggedInUser.email}</span>
			<!-- User's email -->
		</DropdownHeader>

		<!-- Dropdown item for managing subscriptions -->
		<DropdownItem href={manageSubscriptionsLink}>Gestionar suscripciones</DropdownItem>
		<!-- Dropdown item for managing subscribers -->
		<DropdownItem href={manageSubscribersLink}>Gestionar suscriptores</DropdownItem>
		<!-- Dropdown item for managing payment methods -->
		<DropdownItem href={manageCardsLink}>Métodos de pago</DropdownItem>
		<!-- Dropdown item for managing payment methods -->
		<DropdownItem href={managePaymentProcessingLink}>Procesamiento de Pagos</DropdownItem>

		<!-- Divider line within the dropdown menu -->
		<DropdownDivider />

		<!-- Dropdown item for logging out -->
		<DropdownItem on:click={handleLogout}>Cerrar Sesión</DropdownItem>
	</Dropdown>
</div>
