import type { Config } from "tailwindcss";
const config: { plugins: any[]; theme: { extend: {} }; content: string[] } = {
    content: [
        './app/**/*.{js,ts,jsx,tsx}',
        './components/**/*.{js,ts,jsx,tsx}',
        ],
    theme: { extend: {} },
    plugins: [],
}
export default config;
