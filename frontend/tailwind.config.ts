import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "on-secondary-fixed-variant": "#42474b",
        "secondary-fixed-dim": "#c2c7cc",
        "secondary-fixed": "#dfe3e8",
        "primary-fixed": "#d9e2ff",
        "on-primary-fixed": "#001946",
        "primary-container": "#3366cc",
        "inverse-on-surface": "#f2f0f1",
        "tertiary-container": "#bfab49",
        "error-container": "#ffdad6",
        "error": "#ba1a1a",
        "surface-variant": "#e3e2e3",
        "surface-container-high": "#e9e8e9",
        "on-tertiary-fixed-variant": "#524600",
        "on-background": "#1b1c1d",
        "outline-variant": "#c3c6d5",
        "on-secondary-fixed": "#171c20",
        "tertiary-fixed-dim": "#dcc661",
        "on-secondary-container": "#606569",
        "surface-container-highest": "#e3e2e3",
        "on-error": "#ffffff",
        "surface-bright": "#faf9fa",
        "primary": "#094cb2",
        "on-error-container": "#93000a",
        "outline": "#737784",
        "tertiary-fixed": "#f9e37a",
        "on-tertiary": "#ffffff",
        "surface-tint": "#2259bf",
        "on-primary-container": "#e7ebff",
        "surface-container-low": "#f5f3f4",
        "on-surface": "#1b1c1d",
        "on-surface-variant": "#434653",
        "on-primary-fixed-variant": "#00419d",
        "secondary": "#5a5f63",
        "on-tertiary-fixed": "#211b00",
        "background": "#faf9fa",
        "tertiary": "#6d5e00",
        "inverse-surface": "#303031",
        "on-primary": "#ffffff",
        "primary-fixed-dim": "#b1c5ff",
        "inverse-primary": "#b1c5ff",
        "surface-container": "#efedee",
        "on-tertiary-container": "#4a3f00",
        "surface-dim": "#dbdadb",
        "surface-container-lowest": "#ffffff",
        "surface": "#faf9fa",
        "secondary-container": "#dfe3e8",
        "on-secondary": "#ffffff"
      },
      fontFamily: {
        "headline": ["var(--font-noto-serif)", "serif"],
        "display": ["var(--font-noto-serif)", "serif"],
        "body": ["var(--font-inter)", "sans-serif"],
        "label": ["var(--font-public-sans)", "sans-serif"]
      }
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/container-queries")
  ],
};
export default config;
