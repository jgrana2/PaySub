<script>
	import HeaderAvatar from '$lib/components/HeaderAvatar.svelte';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import SubscribersTable from '$lib/components/SubscribersTable.svelte';
	import { Tabs, TabItem } from 'flowbite-svelte';
</script>

<div class="flex bg-gray-50">
	<Sidebar />
	<div class="flex flex-col w-full h-screen">
		<!-- Set a height for the container -->
		<HeaderAvatar title="Suscriptores" />
		<!-- This will stay fixed at the top -->
		<div class="overflow-auto">
			<!-- This div will be scrollable -->
			<Tabs class="px-4">
				<TabItem open title="Mis Suscriptores">
					<div class="overflow-auto">
						<p class="text-sm text-gray-500 dark:text-gray-400">
							<SubscribersTable />
						</p>
					</div>
				</TabItem>
			</Tabs>
		</div>
	</div>
</div>
