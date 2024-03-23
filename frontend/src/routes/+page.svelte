<svelte:head>
	<title>¡Bienvenido a PaySub!</title>
</svelte:head>

<div class="bg-gray-100 p-4">
	<div class="container mx-auto text-center">
		<div class="flex justify-end items-center gap-4 mb-10">
			<a href="login" class="text-blue-500">Iniciar sesión</a>
			<a href="register" class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">Regístrate ahora</a>
		</div>
		<div class="flex justify-center">
			<img src="logo.png" alt="Logo" class="w-16" />
		</div>

		<h1 class="text-4xl font-bold mb-4">PaySub</h1>
		<p class="text-lg text-gray-600">Simple. Directo. Suscripciones Hechas Correctamente.</p>

		<div class="mt-12">
			<h2 class="text-2xl font-semibold mb-4">
				Descubre oportunidades esperando por ti. ¿Estás listo para monetizar tu contenido o servicios?
			</h2>
			<p class="text-gray-700">
				Amplía tu negocio fácilmente, PaySub facilita, efectiva y seguramente para creadores, diseñadores, desarrolladores y pequeñas empresas como tú configurar paquetes de suscripción y compartirlos con el mundo. Ya nos hemos ocupado de las partes difíciles por ti. 
			</p>
		</div>

		<div class="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
			<!-- Crea Tu Paquete -->
			<div class="p-6 bg-white rounded shadow">
				<h3 class="text-xl font-semibold mb-2">Crea Tu Paquete</h3>
				<p class="text-gray-600">
					Diseña opciones de suscripción a medida que se ajusten a tu modelo de negocio. Establece tu precio, duración y niveles de acceso al contenido con facilidad.
				</p>
			</div>

			<!-- Compartir Sin Esfuerzo -->
			<div class="p-6 bg-white rounded shadow">
				<h3 class="text-xl font-semibold mb-2">Comparte Sin Esfuerzo</h3>
				<p class="text-gray-600">
					Genera enlaces únicos para tus paquetes de suscripción. Difunde la noticia a través de redes sociales, correos electrónicos o en tu sitio web.
				</p>
			</div>

			<!-- Experiencia de Suscriptor Impecable -->
			<div class="p-6 bg-white rounded shadow">
				<h3 class="text-xl font-semibold mb-2">Experiencia de Suscriptor Impecable</h3>
				<p class="text-gray-600">
					Los usuarios pueden ver los detalles de la suscripción con un solo clic. Un proceso claro les guía desde el interés hasta la suscripción.
				</p>
			</div>
		</div>

		<div class="mt-12">
			<h2 class="text-2xl font-semibold mb-4">Nuevos Suscriptores: Comienza Inmediatamente</h2>
			<p class="text-gray-700">
				Un proceso de registro simple que te pondrá en marcha. Una interfaz amigable que te tendrá suscrito en poco tiempo.
			</p>
		</div>

		<div class="mt-12">
			<h2 class="text-2xl font-semibold mb-4">Pago Seguro</h2>
			<p class="text-gray-700">
				Agrega tu método de pago sin complicaciones. Confía en pasarelas líderes como MercadoPago para tus transacciones.
			</p>
		</div>

		<div class="mt-12">
			<h2 class="text-2xl font-semibold mb-4">Acceso Instantáneo</h2>
			<p class="text-gray-700">
				Pulsa el botón 'Suscribirse' e inmediatamente sumérgete en tu nuevo contenido. Disfruta siendo parte de una comunidad de suscriptores en constante crecimiento.
			</p>
		</div>

		<div class="mt-12 flex justify-center">
			<img src="subsflow.svg" alt="Diagrama de Flujo de Suscripción" />
		</div>

		<!-- Open Source Project Section -->
        <div class="flex flex-col mt-12 bg-white p-6 rounded shadow">
            <h2 class="text-2xl font-semibold mb-4 text-green-600">Open Source Project</h2>
            <p class="text-gray-700">
                <span class="font-bold">PaySub</span> es un proyecto <span class="text-blue-500">Open Source</span>. Puedes encontrar el repositorio y contribuir en:
            </p>
            <a href="https://github.com/jgrana2/PaySub" class="text-blue-500 hover:text-blue-700">GitHub Repo</a>
            <p class="text-gray-700 mt-4">
                Sigue el desarrollo y las actualizaciones del proyecto en nuestras redes sociales:
            </p>
			<div class="flex justify-center gap-2">
            <a href="https://twitter.com/PaySubApp" class="text-blue-500 hover:text-blue-700">Twitter</a> ·
            <a href="https://www.facebook.com/people/PaySub/61557515165359/" class="text-blue-500 hover:text-blue-700">Facebook</a> ·
            <a href="https://www.instagram.com/paysubapp/" class="text-blue-500 hover:text-blue-700">Instagram</a>
		</div>
        </div>

        <!-- Cloud Hosted Option Section -->
        <div class="flex flex-col mt-12 bg-blue-50 p-6 rounded shadow justify-center items-center">
			<h2 class="text-2xl font-semibold text-blue-600">Cloud Hosted Solution</h2>
			<p class="text-gray-700 m-4 text-center">
				¿Prefieres una opción <span class="font-bold">sin gestión</span>? Prueba nuestra solución alojada en la nube. Crea <span class="underline">números ilimitados</span> de productos, suscripciones y métodos de pago gratis.
			</p>
			<div class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 w-fit mx-auto">
				<a href="register" class="block text-center">Regístrate ahora</a>
			</div>
			<p class="mt-4">
				¿Ya tienes una cuenta? <a href="login" class="text-blue-500">Iniciar sesión</a>
			</p>
		</div>
		

		<div class="mt-12">
			<p class="text-xl font-semibold mb-4">
				Todo el mundo tiene la capacidad de ser propietario de un negocio exitoso. Con nuestra guía, tú también puedes alcanzar el éxito.
				Únase a <span class="text-blue-500">PaySub</span> hoy – ¡donde suscribirse es tan fácil como hacer un click! 🌟
			</p>
			<p class="mb-8">¿Listo para desbloquear contenido exclusivo?</p>
			
		</div>
	</div>

	<div class="text-center mt-8">
		<p class="text-sm text-gray-600">
			Para soporte o consultas, por favor contáctenos en <a href="mailto:soporte@paysub.app" class="text-blue-500">soporte@paysub.app</a>.
		</p>
	</div>
</div>
