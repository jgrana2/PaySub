<script lang="ts">
	import { Plus } from 'svelte-heros-v2';
	import { Button } from 'flowbite-svelte';
</script>

<div class="absolute bottom-0 right-0 mb-4 mr-4 z-10">
	<a href="payment_method">
		<Button
			class="w-16 h-16 rounded-full transition-all shadow hover:shadow-lg transform hover:scale-110 flex items-center justify-center"
		>
			<svelte:component this={Plus}></svelte:component>
		</Button>
	</a>
</div>
