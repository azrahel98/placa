<script setup lang="ts">
	import axios from 'axios'
	import { onMounted, ref } from 'vue'
	const images = ref([])
	const image_preview = ref<null | string>(null)
	const loading = ref(false)

	onMounted(async () => {
		loading.value = true
		const res = await axios('http://127.0.0.1:5000/images', {
			method: 'GET',
			headers: {
				Bearer: localStorage.getItem('token')
			}
		})
		images.value = res.data
		loading.value = false
	})

	const subir = async (e: any) => {
		try {
			loading.value = true
			const formData = new FormData()
			formData.append('file', e.target.files[0])
			await axios.post('http://127.0.0.1:5000/check', formData, {
				headers: {
					'Content-Type': 'multipart/form-data',
					Bearer: localStorage.getItem('token')
				}
			})
			image_preview.value = URL.createObjectURL(e.target.files[0])
			const res = await axios('http://127.0.0.1:5000/images', {
				method: 'GET',
				headers: {
					Bearer: localStorage.getItem('token')
				}
			})
			images.value = res.data
		}   catch (error) {
    console.error('Error detallado:', error)
    if ((error as any).response) {
      console.error('Respuesta del servidor:', (error as any).response.data)
      console.error('Estado HTTP:', (error as any).response.status)
    }
		loading.value = false
	}
}
</script>

<template>
	<div class="">
		<div class="w-full bg-lightPrimary dark:!bg-navy-900 h-full">
			<main class="inicio pt-16">
				<a
					class="place-self-center flex flex-col items-center bg-white border border-gray-200 rounded-lg shadow md:flex-row md:max-w-xl hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700">
					<img
						v-if="image_preview"
						class="object-cover w-full rounded-t-lg h-96 md:h-auto md:w-96 md:rounded-none md:rounded-s-lg"
						:src="image_preview"
						alt="" />
					<div class="flex flex-col justify-between p-4 leading-normal">
						<label
							for="dropzone-file"
							class="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-gray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600">
							<div class="flex flex-col items-center justify-center pt-5 pb-6">
								<svg
									class="w-8 h-8 mb-4 text-gray-500 dark:text-gray-400"
									aria-hidden="true"
									xmlns="http://www.w3.org/2000/svg"
									fill="none"
									viewBox="0 0 20 16">
									<path
										stroke="currentColor"
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2" />
								</svg>
								<p class="mb-2 text-sm text-gray-500 dark:text-gray-400">
									<span class="font-semibold">Click to upload</span>
									or drag and drop
								</p>
								<p class="text-xs text-gray-500 dark:text-gray-400">
									SVG, PNG, JPG or GIF (MAX. 800x400px)
								</p>
							</div>
							<input id="dropzone-file" type="file" @change="subir" class="hidden" />
						</label>
					</div>
				</a>
				<div
					v-if="loading"
					class="flex items-center justify-center w-full h-56 border border-gray-200 rounded-lg bg-gray-50 dark:bg-gray-800 dark:border-gray-700">
					<div
						class="px-3 py-1 text-xs font-medium leading-none text-center text-blue-800 bg-blue-200 rounded-full animate-pulse dark:bg-blue-900 dark:text-blue-200">
						loading...
					</div>
				</div>
				<div
					v-else
					class="fotos mt-8 border border-gray-200 rounded-lg bg-gray-50 dark:bg-gray-800 dark:border-gray-700">
					<a
						v-for="x in images"
						class="flex flex-col items-center bg-white border border-gray-200 rounded-lg shadow md:flex-row md:max-w-xl hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700">
						<img
							class="object-cover w-full rounded-t-lg h-96 md:h-auto md:w-48 md:rounded-none md:rounded-s-lg"
							:src="`data:image/png;base64,${x}`"
							alt="" />
					</a>
				</div>
			</main>
		</div>
	</div>
</template>
<style lang="scss">
	.inicio {
		display: grid;
		grid-template-rows: min-content 1fr;
	}
	.fotos {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(min(100%, 15em), 1fr));
		justify-content: center;
		align-items: center;
		justify-items: center;
	}
</style>
