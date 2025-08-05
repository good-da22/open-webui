<script>
	import { createEventDispatcher } from 'svelte';
	export let isOpen = false;
	export let url = '';

	const dispatch = createEventDispatcher();

	const closeModal = () => {
		dispatch('close');
	};
</script>

{#if isOpen}
	<div class="modal-overlay" on:click={closeModal} aria-hidden={!isOpen}>
		<div class="modal-content" on:click|stopPropagation tabindex="0">
			<img
				src={url}
				alt="첨부파일 로드 실패"
				class="modal-image"
				on:error={() => console.error('첨부파일 로딩 실패:', url)}
			/>
			<button class="close-button" on:click={closeModal} aria-label="Close Modal">&times;</button>
		</div>
	</div>
{/if}

<style>
	.modal-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 1000;

		/* 흐림 효과 */
		backdrop-filter: blur(6px);
		-webkit-backdrop-filter: blur(6px); /* Safari 호환성 */
	}

	.modal-content {
		background: white;
		padding: 1rem;
		border-radius: 8px;
		max-width: 90vw;
		max-height: 90vh;
		position: relative;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;

		/* 얇은 경계선 효과 */
		border: 1px solid rgba(255, 255, 255, 0.15);
		outline: 2px solid rgba(0, 0, 0, 0.1);
		box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
	}
	.modal-image {
		max-width: 100%;
		max-height: 80vh;
		object-fit: contain;
		display: block;
	}
	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: scale(0.9);
		}
		to {
			opacity: 1;
			transform: scale(1);
		}
	}

	.close-button {
		position: absolute;
		top: 10px;
		right: 10px;
		background: transparent;
		color: black;
		border: none;
		font-size: 1.5rem;
		cursor: pointer;
	}
</style>
