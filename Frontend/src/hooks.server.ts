import type { Handle, RequestEvent } from '@sveltejs/kit'
import { accessToken as token } from './stores'


// Attach authorization to each server request (role may have changed)
async function attachUserToRequestEvent(accessToken: string, event: RequestEvent) {
	// const sql = `SELECT * FROM get_session($1);`
	// const { rows } = await query(sql, [sessionId])
	// if (rows?.length > 0) {
	// 	event.locals.user = <User>rows[0].get_session
	// }
	console.log('accessToken', accessToken)
	const response = await fetch('http://localhost:5001/auth/current-user', {
		headers: {
			'Authorization': `Bearer ${accessToken}`,
			'Content-Type': 'application/json',
			'Access-Control-Allow-Origin': '*',
		},
		credentials: 'include',
	})
	if (response.ok) {
		event.locals.user = await response.json();
		console.log('user', event.locals.user)
	}
}

// Invoked for each endpoint called and initially for SSR router
export const handle: Handle = async ({ event, resolve }) => {
	// before endpoint or page is called
	const accessToken = event.cookies.get('accessToken')
	if (accessToken) {
		await attachUserToRequestEvent(accessToken, event)
	}
	console.log(event.locals.user)
	if (!event.locals.user) {
		event.cookies.set('accessToken', '', {
			httpOnly: true,
			sameSite: 'lax',
			path: '/'
		})
	}

	const response = await resolve(event)

	// after endpoint or page is called

	return response
}
