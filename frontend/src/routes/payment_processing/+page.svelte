<script>
	import HeaderAvatar from '$lib/components/HeaderAvatar.svelte';
	import MercadoPagoCredentialsForm from '$lib/components/MercadoPagoCredentialsForm.svelte';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import { Tabs, TabItem } from 'flowbite-svelte';
</script>

<div class="flex bg-gray-50">
	<Sidebar />
	<div class="flex flex-col w-full h-screen"> <!-- Set a height for the container -->
	  <HeaderAvatar title="Procesamiento de Pagos" /> <!-- This will stay fixed at the top -->
	  <div class="overflow-auto"> <!-- This div will be scrollable -->
		<Tabs class="px-4">
			<TabItem open title="Mercado Pago">
				<p class="text-sm text-gray-500 dark:text-gray-400">
					<MercadoPagoCredentialsForm />
				</p>
			</TabItem>
		</Tabs>
	  </div>
	</div>
  </div>
  
