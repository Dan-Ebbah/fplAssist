'use client'
import { useState } from 'react'
import Controls from '@/components/Controls'
import PicksTable from '@/components/PicksTable'
import RationaleCard from '@/components/RationaleCard'
import { getProjections, optimizeXI } from '@/lib/api'

type Proj = any

export default function Page() {
  const [projs, setProjs] = useState<Proj[]>([])
  const [captainId, setCaptainId] = useState<number | undefined>(undefined)
  const [explanation, setExplanation] = useState('')

  async function run({ gw, risk, budget, formation }: { gw: number; risk: number; budget: number; formation: string }) {
    const p = await getProjections(gw, risk)
    setProjs(p.projections)
    const opt = await optimizeXI({ gw, budget, formation, risk_tolerance: risk })
    setCaptainId(opt.captain_id)
    setExplanation(opt.explanation)
  }

  return (
      <main className="grid gap-6">
        <h1 className="text-2xl font-bold">FPL Assistant — MVP</h1>
        <Controls onRun={run} />
        {projs.length>0 && <PicksTable data={projs} captainId={captainId} />}
        {explanation && <RationaleCard text={explanation} />}
        <p className="text-xs text-slate-500">v0.1 — projections use FPL ep_next adjusted by minutes risk; upgradeable to xMins/event-rate model.</p>
      </main>
  )
}
