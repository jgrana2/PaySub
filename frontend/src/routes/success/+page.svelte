<script>
    import Header from '$lib/components/Header.svelte';
</script>

<Header/>
<main class="bg-white h-screen">
    <section class="mx-auto p-6 border rounded-lg max-w-md">
        <svg viewBox="0 0 24 24" class="text-green-600 w-16 h-16 mx-auto my-6">
            <path fill="currentColor" d="M12,0A12,12,0,1,0,24,12,12.014,12.014,0,0,0,12,0Zm6.927,8.2-6.845,9.289a1.011,1.011,0,0,1-1.43.188L5.764,13.769a1,1,0,1,1,1.25-1.562l4.076,3.261,6.227-8.451A1,1,0,1,1,18.927,8.2Z"></path>
        </svg>
        <article class="text-center">
            <h3 class="text-base md:text-2xl text-gray-900 font-semibold">¡Pago hecho!</h3>
            <p class="text-gray-600 my-2">Gracias por completar su pago seguro en línea.</p>
            <p>¡Qué tengas un lindo día!</p>
            <div class="py-10">
                <a href="/login" class="px-12 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-3 rounded">REGRESA</a>
            </div>
        </article>
    </section>
</main>
