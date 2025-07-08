import { paraglideVitePlugin } from '@inlang/paraglide-js';
import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';
import svelteSVG from '@poppanator/sveltekit-svg';

export default defineConfig({
	plugins: [
		tailwindcss(),
		svelteSVG({
			// Optional: svgo options or default true
			// svgo: true,
			// Default: "src/lib/icons"
			// includePaths: ["src/assets/icons"],
			// Default: ".svg"
			// ext: "svg"
		}),
		sveltekit(),
		paraglideVitePlugin({
			project: './project.inlang',
			outdir: './src/lib/paraglide'
		}),
		VitePWA({
			registerType: 'autoUpdate',
			workbox: {
				globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'],
				cleanupOutdatedCaches: true,
				sourcemap: true
			},
			includeAssets: [
				'favicon.ico',
				'apple-touch-icon.png',
				'mask-icon.svg',
				'pwa-192x192.png',
				'pwa-512x512.png'
			],
			manifest: {
				name: 'Majestic',
				short_name: 'Majestic',
				description: 'Kempegowda Bus Station Platform App',
				theme_color: '#ffffff',
				background_color: '#ffffff',
				display: 'standalone',
				orientation: 'portrait',
				scope: '/',
				start_url: '/',
				icons: [
					{
						src: 'pwa-192x192.png',
						sizes: '192x192',
						type: 'image/png',
						purpose: 'any maskable'
					},
					{
						src: 'pwa-512x512.png',
						sizes: '512x512',
						type: 'image/png',
						purpose: 'any maskable'
					}
				]
			},
			devOptions: {
				enabled: true,
				type: 'module'
			}
		})
	],
	server: {
		host: true
	}
});
