import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'


function check ():boolean{

		try {
			if (localStorage.getItem('token')) {
				
				return true
			}
			return false
		} catch (error) {
			console.log(error)
			return false
		}
	
}


const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: '/',
			name: 'home',
			component: HomeView,
			beforeEnter: (to, from, next) => {
				const loged = check()
				if (!loged) {
					next('/login')
					return
				}
				next()
			},
		},
		{
			path: '/login',
			name: 'login',
			component: () => import('../views/login.vue')
		}
	]
})

export default router
