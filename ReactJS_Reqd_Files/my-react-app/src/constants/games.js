// this is for the games list (shared between CreateServer)

export const GAMES = [
  { key: 'minecraft', label: 'Minecraft (Java Edition)' },
  { key: 'rust',      label: 'Rust' },
  { key: 'ark',       label: 'ARK: Survival Evolved' },
  { key: 'csgo',      label: 'Counter-Strike: Global Offensive' },
  { key: 'factorio',  label: 'Factorio' },
]

export const GAME_DEFAULTS = {
  minecraft: { serverPort: 25565, rconPort: 25575, queryPort: 25565 },
  rust:      { serverPort: 28015, rconPort: 28016, queryPort: 28015 },
  ark:       { serverPort: 7777,  rconPort: 27020, queryPort: 27015 },
  csgo:      { serverPort: 27015, rconPort: 27015, queryPort: 27015 },
  factorio:  { serverPort: 34197, rconPort: 27015, queryPort: 34197 },
}

export const GAME_EXTRAS = {
  minecraft: [
    { name: 'maxPlayers', label: 'Max players', type: 'number', placeholder: 'e.g., 20' },
    { name: 'seed',       label: 'World seed',  type: 'text',   placeholder: 'optional' },
  ],
  rust: [
    { name: 'worldSeed',  label: 'World seed',  type: 'number', placeholder: 'e.g., 12345' },
    { name: 'worldSize',  label: 'World size',  type: 'number', placeholder: 'e.g., 3500' },
  ],
  ark: [
    { name: 'map',           label: 'Map',            type: 'text',     placeholder: 'e.g., TheIsland' },
    { name: 'adminPassword', label: 'Admin password', type: 'password', placeholder: 'optional' },
  ],
  csgo: [
    { name: 'tickrate', label: 'Tick rate', type: 'number', placeholder: 'e.g., 128' },
    { name: 'map',      label: 'Start map', type: 'text',   placeholder: 'e.g., de_dust2' },
  ],
  factorio: [
    { name: 'saveName', label: 'Save name', type: 'text', placeholder: 'e.g., factory-01' },
    { name: 'mods',     label: 'Mods list', type: 'text', placeholder: 'comma-separated' },
  ],
}
