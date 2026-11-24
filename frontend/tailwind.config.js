/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0f172a",
        foreground: "#f8fafc",
        card: "#1e293b",
        border: "#334155",
        primary: {
          DEFAULT: "#3b82f6",
          hover: "#2563eb",
        },
        accent: "#10b981",
        muted: "#94a3b8"
      }
    },
  },
  plugins: [],
};
