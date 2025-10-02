export default function Games() {
  const games = [
    'Minecraft (Java Edition)',
    'Rust',
    'ARK: Survival Evolved',
    'Factorio',
    'Counter-Strike: Global Offensive',
    'Team Fortress 2',
    "Garry's Mod",
    'Left 4 Dead 2',
    'Squad',
  ]

  return (
    <main>
      <h1>RCON-Compatible Games</h1>
      <ul>
        {games.map(name => (
          <li key={name}>{name}</li>
        ))}
      </ul>
    </main>
  )
}

// each game is just text for now.

// this file will probably not change after this, unless I see a way for an
// api to fetch compatible games... but I im not sure.
// complete 10.2.25