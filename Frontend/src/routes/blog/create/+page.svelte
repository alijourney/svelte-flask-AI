<script lang="ts">
	import type { PageData } from './$types'
	import { toast, accessToken } from '../../../stores'

    export let data: PageData
	let title: string = ''
	let text: string = ''
	let selectedCategory: string = ''
    const { categories }: { categories: Category[] } = data

	async function handleSubmit() {
		console.log('[accessToken]',  $accessToken)
		const res = await fetch('http://localhost:5001/blog/create-blog', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*',
				'Authorization': `Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMzQ3NTc2MiwianRpIjoiNzlhYzAwM2ItMGU3OC00NTJiLTg2NTctMzQ0NWM5M2M3YTVlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImM5MTViOTE1LTM3NTEtNDg4ZC1iODJkLTdiZGE4ZDBkZjhlZSIsIm5iZiI6MTcyMzQ3NTc2MiwiZXhwIjoxNzIzNDc2NjYyfQ.8mgl_6SnfsPSHfROzTOBygPxlwWIt09a_XAQboDsTtA`
			},
			credentials: 'include',
			body: JSON.stringify({
				title: title,
				text: text,
				category_id: selectedCategory,
			})
		})
		if (res.ok) {
			$toast = {
				title: 'submit successfully',
				body: 'submit successfully',
				isOpen: true
			}
		}
	}
</script>

<svelte:head>
	<title>Create Blog</title>
</svelte:head>

<h1>Create blog</h1>
<form method="POST">
	Title: <input type="text" name="title" bind:value={title}/>
	Text: <input type="text" name="ext" bind:value={text}/>
	<select class="form-select" bind:value={selectedCategory}>
        {#each categories as category}
            <option
                value={category.id}
            >
                {category.name}
            </option>
        {/each}
    </select>
	<button on:click|preventDefault={async () => { await handleSubmit() }} value="submit">Submit</button>
</form>