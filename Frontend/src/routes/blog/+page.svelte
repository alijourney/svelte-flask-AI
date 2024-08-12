<script lang="ts">
    import { goto } from '$app/navigation'
	import type { PageData } from './$types'

    export let data: PageData
    const { categories }: { categories: Category[] } = data
    let { blogs } : { blogs: Blog[] } = data
    let selectedCategory: string = ''
    async function handleCategoryChange() {
        const blogsResponse = await fetch(`http://localhost:5001/blog/category/${selectedCategory}`, {
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            credentials: 'include',
        })
        if (blogsResponse.ok) {
            blogs = (await blogsResponse.json())['blogs']
        }
    }
</script>

<svelte:head>
	<title>Blog</title>
</svelte:head>

<div>
    <h1>Blogs</h1>
    <select class="form-select" bind:value={selectedCategory} on:change={handleCategoryChange}>
        {#each categories as category}
            <option
                value={category.id}
            >
                {category.name}
            </option>
        {/each}
    </select>
    <button on:click={() => goto('/blog/create')}>Create Blog</button>
    {#each blogs as blog}
        {blog.title}-{blog.text}-{blog.user?.name}-{blog.category.name}
    {/each}
</div>
