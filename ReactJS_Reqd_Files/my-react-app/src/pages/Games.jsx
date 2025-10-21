import { GAMES } from '@/constants/games.js'

export default function Games() {
  return (
    <main>
      <h1>RCON-Compatible Games</h1>
      <ul>
        {GAMES.map(g => (
          <li key={g.key}>{g.label}</li>
        ))}
      </ul>
    </main>
  )
}