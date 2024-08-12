import { redirect } from '@sveltejs/kit'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async (event) => {
	const { user } = event.locals // populated by /src/hooks.ts

    const authorized = ['admin', 'staff'] // must be logged-in
	if (!user || !authorized.includes(user.role)) {
		redirect(302, '/login?referrer=/blog')
	}
    const categoriesResponse = await fetch('http://localhost:5001/blog/get-categories', {
		headers: {
			'Content-Type': 'application/json',
			'Access-Control-Allow-Origin': '*',
		},
		credentials: 'include',
	})
    let categories = []
    if (categoriesResponse.ok) {
        categories = (await categoriesResponse.json())['categories']
    }

    const blogsResponse = await fetch('http://localhost:5001/blog/', {
		headers: {
			'Content-Type': 'application/json',
			'Access-Control-Allow-Origin': '*',
		},
		credentials: 'include',
	})
    let blogs = []
    if (blogsResponse.ok) {
        blogs = (await blogsResponse.json())['blogs']
    }

	return {
        categories,
        blogs
	}
}
