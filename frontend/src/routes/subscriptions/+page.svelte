<script>
	import HeaderAvatar from '$lib/components/HeaderAvatar.svelte';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import SubscriptionsTable from '$lib/components/SubscriptionsTable.svelte';
	import AddSubscription from '$lib/components/AddSubscription.svelte'; // Add this import for the AddSubscription
	import { Tabs, TabItem } from 'flowbite-svelte';
	import ActiveSubscriptionsTable from '$lib/components/ActiveSubscriptionsTable.svelte';
</script>

<div class="flex bg-gray-50">
	<Sidebar />
	<div class="flex flex-col w-full h-screen">
		<HeaderAvatar title="Catálogo" />
		<AddSubscription />
		<div class="overflow-auto">
			<Tabs class="px-4">
				<TabItem open title="Mis Suscripciones">
					<div class="overflow-auto">
						<p class="text-sm text-gray-500 dark:text-gray-400">
							<SubscriptionsTable />
						</p>
					</div>
				</TabItem>
				<TabItem title="Suscripciones Activas">
					<div class="overflow-auto">
						<p class="text-sm text-gray-500 dark:text-gray-400">
							<ActiveSubscriptionsTable />
						</p>
					</div>
				</TabItem>
			</Tabs>
		</div>
	</div>
</div>
