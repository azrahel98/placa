<script setup lang="ts">
	import { RouterView } from 'vue-router'
</script>

<template>
	<div class="mains">
		<router-view />
		<div class="font-mono mx-4 text-xs flex justify-end items-center gap-2"></div>
	</div>
</template>
<style lang="scss" scoped>
	.mains {
		height: 100vh;
		display: grid;
		grid-template-rows: auto min-content;
	}
</style>
