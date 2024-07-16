<template>
	<main class="h-auto">
		<div class="relative flex h-full">
			<div
				class="flex h-full w-full items-center justify-center px-2 md:mx-0 md:px-0 lg:mb-10 lg:items-center lg:justify-center">
				<div
					class="w-full max-w-full flex-col items-center lg:pl-0 md:max-w-[300px] xl:max-w-[420px]">
					<h4 class="mb-2.5 text-4xl font-bold text-center text-navy-700 dark:text-white">
						Iniciar Sesion
					</h4>

					<div class="mb-6 flex items-center gap-0">
						<div class="h-px w-full bg-gray-200 dark:bg-navy-700" />
						<div class="h-px w-full bg-gray-200 dark:bg-navy-700" />
					</div>
					<div class="mb-3">
						<label for="email">Nombre*</label>
						<input
							type="text"
							id="email"
							v-model="form.username"
							placeholder="rscl"
							class="input"
							autocomplete="off"
							:class="{ 'border-red-500': errores?.username != null }" />
						<div v-if="errores?.username" class="text-red-500 flex flex-col text-xs">
							<span v-for="er in errores.username?._errors">{{ er }}</span>
						</div>
					</div>
					<div class="mb-3">
						<label for="password">Contraseña*</label>
						<input
							type="password"
							id="password"
							v-model="form.password"
							placeholder="Min. 8 characters"
							class="input"
							:class="{ 'border-red-500': errores?.password != null }" />
						<div v-if="errores?.password" class="text-red-500 flex flex-col text-xs">
							<span v-for="er in errores.password?._errors">{{ er }}</span>
						</div>
					</div>

					<div class="flex justify-center w-full">
						<button
							class="button1 w-52"
							:class="{ 'bg-red-500': loading }"
							type="button"
							@click="login"
							:disabled="loading">
							Login
						</button>
					</div>
					<div class="mt-4">
						<span class="text-sm font-medium text-navy-700 dark:text-gray-600">
							No estas registrado?, pide tu registro
						</span>
					</div>
				</div>
			</div>
		</div>
	</main>
</template>
<script lang="ts" setup>
	import { reactive, ref } from 'vue'
	import * as z from 'zod'
	import router from '../router/index'
	import axios from 'axios'

	const form = reactive({
		username: '',
		password: ''
	})

	const loading = ref(false)

	const formSchema = z.object({
		username: z.string().min(1, { message: 'No debe ser vacio' }),
		password: z.string().min(1, { message: 'No debe ser vacio' })
	})

	type formSchemaType = z.infer<typeof formSchema>
	const errores = ref<z.ZodFormattedError<formSchemaType> | null>(null)

	const login = async () => {
		loading.value = true
		try {
			const valid = formSchema.safeParse(form)
			errores.value = null

			if (!valid.success) {
				errores.value = valid.error.format()
			} else {
				const res = await axios('http://127.0.0.1:5000/login', {
					method: 'POST',
					data: {
						username: form.username,
						password: form.password
					}
				})

				localStorage.setItem('token', res.data.token)

				await router.push({ name: 'home' })
			}
		} catch (error) {
			var er = error as any
			if (er.response.data.message == 'Usuario no existe') {
				errores.value = {
					_errors: [],
					username: {
						_errors: ['Usuario no existe']
					}
				}
			} else if (er.response.data.message == 'Password Incorrecta') {
				errores.value = {
					_errors: [],
					password: {
						_errors: ['Password Incorrecta']
					}
				}
			}
		}
		loading.value = false
	}
</script>
