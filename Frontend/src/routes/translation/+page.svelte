<script lang="ts">
	let text: string = ''
    let result: string = ''

	async function handleSubmit() {
		const res = await fetch('http://localhost:5001/translate/create', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*',
			},
			credentials: 'include',
			body: JSON.stringify({
				text
			})
		})
		if (res.ok) {
            result = (await res.json())['data'].response
		}
	}
</script>

<svelte:head>
	<title>Translation</title>
</svelte:head>

<h1>Transation</h1>
<form method="POST">
	Text: <textarea name="title" bind:value={text}/>
	<button on:click|preventDefault={async () => { await handleSubmit() }}>Translate</button>
</form>
<textarea name="result" bind:value={result}></textarea>