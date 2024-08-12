// @ts-nocheck
import { redirect } from '@sveltejs/kit'
import type { PageServerLoad } from './$types'

export const load = ({ locals }: Parameters<PageServerLoad>[0]) => {
	const { user } = locals
	if (user) {
		// Redirect to home if user is logged in already
		redirect(302, '/')
	}
	return {}
}
