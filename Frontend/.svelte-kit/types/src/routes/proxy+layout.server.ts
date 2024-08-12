// @ts-nocheck
import type { LayoutServerLoad } from './$types'

export const load = ({ locals }: Parameters<LayoutServerLoad>[0]) => {
	const { user } = locals // locals.user set by hooks.server.ts/handle(), undefined if not logged in
	return {
		user
	}
}
