// mock data

// Create server
if (method === 'POST' && url === '/api/servers') {
  const bodyObj = body || {}
  const nextId = Math.max(0, ...SERVERS.map(s => s.id)) + 1
  const game = bodyObj.game || bodyObj?.connection?.game || 'minecraft'
  const name = bodyObj.name || `Server #${nextId}`

  const newServer = {
    id: nextId,
    name,
    game,
    status: 'offline',
    players: 0,
    maxPlayers: bodyObj?.extras?.maxPlayers ?? null,
    uptimeSec: 0,
    // Keep a little shape for detail page
    connection: {
      host: bodyObj?.connection?.host ?? 'localhost',
      serverPort: bodyObj?.connection?.serverPort ?? 25565,
      rcon: { port: bodyObj?.connection?.rcon?.port ?? 25575 },
      queryPort: bodyObj?.connection?.queryPort ?? 25565
    },
    paths: bodyObj?.paths || null,
    extras: bodyObj?.extras || {},
  }
  SERVERS.push(newServer)
  return newServer
}
