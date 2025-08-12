export default function RationaleCard({ text }: { text: string }) {
    return (
        <div className="rounded-2xl bg-white p-4 shadow">
            <h3 className="mb-2 text-lg font-semibold">Why these picks?</h3>
            <p className="text-sm text-slate-700 whitespace-pre-line">{text}</p>
        </div>
    )
}
