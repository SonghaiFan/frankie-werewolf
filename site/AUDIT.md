# Werewolf introduction audit

Audited 2026-11-06. Scope is `site/` and relevant Pages input watches only. App source, game behavior, dependency files and hosting configuration remain unchanged.

## Design read

Reading this as a local-party-game introduction, preserving the actual zinc-dark control room, indigo controls, rounded panels, heavy sans title and monospace identity numbers. Variance 5, motion 1, density 4. Native CSS follows `client/src/index.css`; the dark page preserves the landing/night identity while screenshots show genuine current UI. The game itself changes to a light daytime theme. No invented pink palette, generated UI or new dependency is introduced.

## Actual app opened

Built the current client with `npm run build --prefix client`. Started the same Express/Socket.IO/game implementation on loopback port 8345. To avoid publishing a LAN listener during the audit, a temporary `/tmp/werewolf-intro-runtime/server/server.js` copy changed only its listen address from `0.0.0.0` to `127.0.0.1`; tracked source was never edited. Game modules and built client were linked from the current repository.

Opened the real landing and host configuration, selected a preset, created a harmless Demo Host room, and joined it as Demo Player through a second browser origin. Clicked Ready; verified the host's Start Game button became enabled and inspected editable host settings. Captured genuine landing/setup/host/player screenshots; the player capture uses an actual 390px target viewport. These are two local browser clients, not two physical phones, a physical Wi-Fi test, or a complete six-player match. No full day/night game or spoken-audio validation is claimed.

The very first game-state event can arrive before `GameRoom` subscribes, briefly showing a generic waiting view; the next player/readiness broadcast populated host controls. This observed timing behavior was not changed as part of the intro.

## Source evidence

- `server/server.js`: Express serves `client/dist`, Socket.IO room lifecycle, in-memory `Map`, personalised broadcasts, dynamic port selection and `.port` file, same-server latest-room discovery.
- `client/vite.config.js`, `client/src/socket.js`: Vite LAN host and Socket.IO proxy using `.port`; production client connects to its own origin.
- `client/src/components/Landing.jsx`, `App.jsx`: host/join flows, names, room query, `sessionStorage` player/room reconnect identifiers and error recovery. No account or persistent match archive is present.
- `GameSettings.jsx`: exact 6/9/12 presets and role/win toggles. The intro build reads these source compositions, adds remaining Villager slots and fails if required presets disappear.
- `RoleIcons.jsx`: original role SVGs extracted at build time, not redrawn. `site/demo.js` changes only a clearly labelled unsaved preset explainer.
- `server/game/RoleDefinitions.js`, `roles/*.js`: six roles, their night actions, Guard restrictions, Witch save/poison limits and Hunter poison exception.
- `utils/roleDeck.js`, `utils/nightFlow.js`: deck balancing for actual participant count and role-priority-driven night ordering.
- `utils/winLogic.js`: good wins at zero wolves; wolf parity/majority check applies to both modes; Side Kill additionally checks ordinary villagers or special good roles. This distinction is explained instead of repeating the Wipeout label as a complete rule.
- `GameFlow.js`, `managers/DayManager.js`, `panels/DayPanel.jsx`: speaking order, votes, tied-candidate speeches/revotes, elimination and last words.
- `utils/stateView.js`: own-role and wolf-team information, broader dead-player/end-game visibility. The intro does not promise a hardened anti-cheat system.
- `useVoiceJudge.js`, `voiceMessages.js`: only the host speaks Chinese browser-synthesised cues; selecting English UI does not translate the spoken script.
- `GameRoom.jsx`, `index.css`: current dark/light phase themes, zinc/indigo tokens, rounded hierarchy and responsive player/control layout.

These are explanations of this implementation, not claims of parity with a particular commercial Werewolf edition. No external rules text or scientific claim is needed; owning code is the primary source.

## Validation

- Current actual client build passed. Vite reported existing Browserslist age and Node deprecation warnings, without build failures; dependencies were not upgraded.
- Standard-library `python3 site/build.py --out /tmp/werewolf-intro-preview` creates EN root and `zh/` independently of app/server/env files.
- Local asset/link checker: two pages, zero issues. `node --check site/demo.js` and `git diff --check` passed.
- Opened the generated intro in Ego. Desktop 1468px had no horizontal overflow. All three lineup controls produced exact 6/9/12 totals and one selected state; the Guard disclosure opened.
- EN and Chinese actual 390×844 target viewports had `scrollWidth === innerWidth === 390`; screenshots visually reviewed. Per-page device overrides cleared.
- All images were loaded during gallery review. No Lighthouse score, physical-LAN interoperability, audio quality or full-match test is claimed.
