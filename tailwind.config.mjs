/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: 'rgb(250, 235, 230)',
          100: 'rgb(245, 220, 215)',
          200: 'rgb(240, 205, 200)',
          300: 'rgb(230, 175, 160)',
          400: 'rgb(220, 145, 120)',
          500: 'rgb(178, 101, 84)',
          600: 'rgb(160, 91, 76)',
          700: 'rgb(140, 80, 67)',
          800: 'rgb(120, 70, 59)',
          900: 'rgb(100, 60, 50)',
        },
        accent: {
          50: 'rgb(250, 240, 240)',
          100: 'rgb(245, 230, 230)',
          200: 'rgb(240, 210, 210)',
          300: 'rgb(230, 180, 180)',
          400: 'rgb(220, 150, 150)',
          500: 'rgb(178, 101, 84)',
          600: 'rgb(160, 91, 76)',
          700: 'rgb(140, 80, 67)',
          800: 'rgb(120, 70, 59)',
          900: 'rgb(100, 60, 50)',
        },
        gray: {
          50: '#f9fafb',
          100: '#f3f4f6',
          200: '#e5e7eb',
          300: '#d1d5db',
          400: '#9ca3af',
          500: '#6b7280',
          600: '#4b5563',
          700: '#374151',
          800: '#1f2937',
          900: '#111827',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      maxWidth: {
        'container': '1200px',
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}