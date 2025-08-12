'use client'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

type Projection = {
    player: {
        id: number;
        name: string;
        team: string;
        position: string;
        price: number;
    }
    xpts_mean: number;
}

export default function PicksTable({ data, captainId}: {data: Projection[]; captainId?: number}) {
    const top = data.slice(0, 10);
    const charData = top.map(p => ({name: p.player.name.split(' ').slice(-1)[0], xpts: p.xpts_mean}));
    return (
        <div className="grid gap-4">
            <div className="rounded-2xl bg-white p-4 shadow">
                <h3 className="mb-2 text-lg font-semibold">Top projections</h3>
                <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={charData}>
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Bar dataKey="xPts" />
                    </BarChart>
                </ResponsiveContainer>
            </div>
            <div className={`rounded-2xl bg-white p-4 shadow`}>
                <h3 className={`mb-2 text-lg font-semibold `}> XI (captain starred)</h3>
                <table className="w-full text-sm">
                    <thead>
                    <tr>
                        <th className="text-left">Name</th>
                        <th>Team</th>
                        <th>Position</th>
                        <th>Price (£m)</th>
                        <th>xPts</th>
                    </tr>
                    </thead>
                    <tbody>
                    {top.map(p => (
                        <tr key={p.player.id} className="border-t">
                            <td className="text-left">
                                {p.player.name} {p.player.id === captainId? ' ⭐️' : ''}
                            </td>
                            <td className="text-center">{p.player.team}</td>
                            <td className="text-center">{p.player.position}</td>
                            <td className="text-center">{p.player.price.toFixed(1)}</td>
                            <td className="text-center">{p.xpts_mean.toFixed(2)}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </div>
    )
}
