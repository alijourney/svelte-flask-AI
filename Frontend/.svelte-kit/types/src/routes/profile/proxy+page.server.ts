// @ts-nocheck
import { redirect } from '@sveltejs/kit'
import type { PageServerLoad } from './$types'

export const load = async ({ locals }: Parameters<PageServerLoad>[0]) => {
	const { user } = locals // populated by /src/hooks.ts

	const authorized = ['admin', 'staff'] // must be logged-in
	if (!user || !authorized.includes(user.role)) {
		redirect(302, '/login?referrer=/profile')
	}

	return {
		user
	}
}
