import type { Config } from "tailwindcss";
const config: { plugins: any[]; theme: { extend: {} }; content: string[] } = {
    content: [
        './app/**/*.{ts,tsx}',
        './components/**/*.{ts,tsx}',
        ],
    theme: { extend: {} },
    plugins: [],
}
export default config;
