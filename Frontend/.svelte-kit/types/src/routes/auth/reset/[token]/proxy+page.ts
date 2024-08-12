// @ts-nocheck
import type { PageLoad } from './$types'

export const load = async( event: Parameters<PageLoad>[0]) => {
	return {
		token: event.params.token
	}
}
