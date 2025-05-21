// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',          // force dark mode via a `.dark` on <html>
  content: [
    './app/templates/**/*.html',
    './app/static/**/*.js',   // if you ever pull classes from planner.js
  ],
  theme: {
    extend: {
      colors: {
        brand: { DEFAULT: '#3b82f6', light: '#93c5fd' },
        surface: { DEFAULT: '#1e293b', light: '#f8fafc' },
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
