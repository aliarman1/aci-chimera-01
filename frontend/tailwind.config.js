/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Techy dark theme colors
        'dark-bg': '#0a0e1a',
        'dark-surface': '#131829',
        'dark-elevated': '#1a1f3a',
        'accent-cyan': '#00d9ff',
        'accent-purple': '#b444ff',
        'accent-pink': '#ff006e',
        'text-primary': '#e2e8f0',
        'text-secondary': '#94a3b8',
        'border-color': '#1e293b',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-tech': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'gradient-cyber': 'linear-gradient(135deg, #00d9ff 0%, #b444ff 100%)',
      },
      boxShadow: {
        'glow-cyan': '0 0 20px rgba(0, 217, 255, 0.3)',
        'glow-purple': '0 0 20px rgba(180, 68, 255, 0.3)',
      },
    },
  },
  plugins: [],
}
