<script>
	import Logo from "./Logo.svelte";
	import { UserGroup, CalendarDays, Briefcase, Home, CreditCard } from 'svelte-heros-v2';
</script>
<div class="flex flex-col min-w-52 h-screen bg-gray-200 hidden lg:block ">
	<p class="text-gray-500 dark:text-gray-400">
	<Logo></Logo>
	<button class="flex w-full justify-left h-16 items-center px-4 rounded hover:bg-slate-300">
		<svelte:component this="{Home}" size="25" class="flex-shrink-0"/> 
		<span class="pl-4">Inicio</span>
	</button>
	<a href="subscribers" class="flex w-full justify-left h-16 items-center px-4 rounded hover:bg-slate-300">
		<svelte:component this="{UserGroup}" size="25" class="flex-shrink-0"/> 
		<span class="pl-4">Usuarios</span>
	</a>
	<a href="subscriptions" class="flex w-full justify-left h-16 items-center px-4 rounded hover:bg-slate-300">
		<svelte:component this="{CalendarDays}" size="25" class="flex-shrink-0"/> 
		<span class="pl-4">Catálogo</span>
	</a>
	<a href="cards" class="flex w-full justify-left h-16 items-center px-4 rounded hover:bg-slate-300">
		<svelte:component this="{CreditCard}" size="25" class="flex-shrink-0"/> 
		<span class=" pl-4">Métodos de Pago</span>
	</a>
	<a href="payment_processing" class="flex w-full justify-left h-16 items-center px-4 rounded hover:bg-slate-300">
		<svelte:component this="{Briefcase}" size="25" class="flex-shrink-0"/> 
		<span class=" pl-4">Procesamiento de Pagos</span>
	</a>
</p>
</div>