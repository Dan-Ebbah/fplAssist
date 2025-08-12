'use client'
import { useState } from 'react';

type Props = {
    onRun: (opts: {gw: number; risk: number; budget: number; formation: string}) => void;
}

export default function Controls({onRun}: Props) {
    const [gw, setGw] = useState(1);
    const [risk, setRisk] = useState(0.5);
    const [budget, setBudget] = useState(100);
    const [formation, setFormation] = useState('3-4-3');

    return (
        <div className="grid gap-4 rounded-2xl bg-white p-4 shadow">
            <div className="grid grid-cols-2 gap-4" >
                <label className="flex items-center gap-2">GW
                    <input type="number" min={1} value={gw} onChange={e => setGw(parseInt(e.target.value||'1'))} className="input" />
                </label>
                <label className="flex items-center gap-2">Budget (£m)
                    <input type="number" min={50} step={0.1} value={budget} onChange={e => setBudget(parseFloat(e.target.value||'100'))} className="input" />
                </label>
            </div>
            <label>Risk tolerance: {risk.toFixed(2)}
                <input type="range" min={0} max={1} step={0.05} value={risk} onChange={e => setRisk(parseFloat(e.target.value))} className="w-full"/>
            </label>
            <label>Formation
                <select className="input" value={formation} onChange={e => setFormation(e.target.value)}>
                    <option>3-4-3</option>
                    <option>3-5-2</option>
                    <option>4-3-3</option>
                    <option>4-4-2</option>
                </select>
            </label>
            <button onClick={()=> onRun({gw, risk, budget, formation})} className="rounded-xl px-4 py-2 bg-slate-900 text-white">Optimize XI</button>
        </div>
    )
}
