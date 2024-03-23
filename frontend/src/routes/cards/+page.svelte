<script>
	import AddCard from '$lib/components/AddCard.svelte';
	import CardsTable from '$lib/components/CardsTable.svelte';
	import HeaderAvatar from '$lib/components/HeaderAvatar.svelte';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import { Tabs, TabItem } from 'flowbite-svelte';
</script>

<div class="flex bg-gray-50">
	<Sidebar />
	<div class="flex flex-col w-full h-screen">
		<!-- Set a height for the container -->
		<HeaderAvatar title="Métodos de Pago" />
		<!-- This will stay fixed at the top -->
		<AddCard />
		<div class="overflow-auto">
			<!-- This div will be scrollable -->
			<Tabs class="px-4">
				<TabItem open title="Tarjetas de Crédito/Débito">
					<p class="text-sm text-gray-500 dark:text-gray-400">
						<CardsTable />
					</p>
				</TabItem>
			</Tabs>
		</div>
	</div>
</div>
