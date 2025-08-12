export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/";
export async function getProjections(gw: number, risk = 0.5){
    const res = await fetch(`${API_BASE}projections?gw=${gw}?risk=${risk}`, {cache: 'no-store'});
    if (!res.ok) {
        throw new Error(`Failed to load projections: ${res.statusText}`);
    }
    return res.json();
}

export async function optimizeXI(body: any) {
    const res = await fetch(`${API_BASE}optimize_xi`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
    });
    if (!res.ok) {
        throw new Error(`Failed to optimize XI: ${res.statusText}`);
    }
    return res.json();
}
