# Werewolf intro maintenance / 狼人杀介绍页维护

The independent Pages site explains the current local game. English is `/`, Chinese is `/zh/`. It never connects a visitor to a room automatically. / 介绍页独立运行，不会自动替访客连接或创建房间。

## Change the right source / 更新对应来源

- `site/content.json`: bilingual explanations, captions, role descriptions, setup and limitations. Recheck source behavior before making a claim.
- `site/build.py`: page structure, exact gallery copies and source extraction. It reads the actual presets from `client/src/components/GameSettings.jsx` and original role icons from `RoleIcons.jsx`. Keep the parser fail-fast when preset syntax changes.
- `site/demo.js`: unsaved preset preview only. It must not assign real roles, emit sockets or pretend to run the game.
- `site/style.css`: intro layout, zinc-dark/indigo surfaces, readable text and phone collapse. Match real tokens in `client/src/index.css`; retain focus and reduced-motion behavior.

中英文文案必须同步核对实际代码。人数预设与角色图标直接从应用源码提取；预览不能伪装为真实开局，也不能产生网络房间。

## Assets to replace / 哪些素材要更新

| Asset | Replace when | Owning UI |
| --- | --- | --- |
| `site/assets/home-current.png` | Name, title, host/join entry changes | `Landing.jsx`, `landing/HomeView.jsx`, `LandingHeader.jsx` |
| `site/assets/setup-current.png` | Presets, role switches or win labels change | `GameSettings.jsx`, `landing/HostView.jsx` |
| `site/assets/host-current.png` | Host settings, ready/start or room layout changes | `WaitingPanel.jsx`, `GameRoom.jsx`, `AvatarCard.jsx` |
| `site/assets/player-current.png` | Mobile waiting/ready layout changes | `WaitingPanel.jsx`, `GameRoom.jsx` |
| `docs/readme/banner.png` | Approved family banner refreshed | Copied to Open Graph image |
| `docs/readme/assets/frankie.svg` | Approved signature changes | Footer artwork |

Capture real settled UI using harmless demo names and a disposable local room. Never capture personal rooms, private identities from an active party, real network addresses or a reusable personal session identifier. The current captures are two local browser clients; captions explicitly avoid claiming a full party. Wait for settings/state broadcasts to settle, and verify the displayed toggles before recording. Hero crop is `.hero-screen img`; adjust crop rather than redrawing a UI.

录制时使用无个人信息的演示昵称与临时房间；等待动画与状态同步完成。手机截图使用真实浏览器窄视口。不要把两台本地浏览器的连接演示写成完整多人对局或实机 Wi-Fi 测试。

## Recheck rules and audio / 行为、规则与语音

- Roles: `server/game/roles/*.js`, `RoleDefinitions.js`, `utils/roleDeck.js` and `utils/nightFlow.js`. Keep Guard, Witch and Hunter exceptions precise.
- Winning rules: `utils/winLogic.js`. Both modes currently include wolf parity; the UI's Wipeout text alone is incomplete.
- Day progression: `GameFlow.js`, `managers/DayManager.js`, `panels/DayPanel.jsx`; verify speeches, voting, ties and last words after changes.
- Role visibility: `utils/stateView.js`; recheck what living/dead/finished clients see.
- Judge voice: `client/src/hooks/useVoiceJudge.js` + `server/game/voiceMessages.js`. It uses host browser speech synthesis with Chinese cues, not recorded audio assets or English narration. If replaced by files later, list every real audio file and required language variant here.
- Persistence: `server/server.js`, `client/src/App.jsx`, `Landing.jsx`. Room memory and tab-session reconnect are not cloud saves.

修改角色、胜负、阶段或语音后，要同时更新文案与预览数据。界面英文与中文法官语音是两个不同的功能，不能混为一谈。

## Run the actual app / 运行真实应用

```sh
npm ci
npm start
```

Open the frontend URL printed by Vite (normally 5173). Other phones must use the host computer's LAN address on the same Wi-Fi, not `localhost`. The backend starts from 3000 and tries another free port; Vite reads `.port` for its proxy. Keep both processes and the computer running. Check firewall access and client isolation on guest networks.

A built-client alternative:

```sh
npm run build --prefix client
npm run server
```

Express serves `client/dist` and Socket.IO together from its actual selected port. Pages is the introduction only; no Vercel runtime is provisioned. / GitHub Pages 只负责介绍页，游戏仍需本地服务器。

## Build, check and publish / 构建、检查、发布

```sh
python3 site/build.py
python3 -m http.server 8080 --directory _site --bind 127.0.0.1
node --check site/demo.js
```

Inspect EN and Chinese at desktop and 390px width. Click all three preset controls and check summed role counts, role disclosures, keyboard focus, images, links and no horizontal overflow. Check the actual app separately if its behavior changed. Source-watch paths in `.github/workflows/pages.yml` refresh the preset/icon extraction; screenshots still require manual replacement.

Commit reviewed `site/` and necessary workflow changes, then push `main`. Never include environment files or unrelated work. / 只提交审阅后的介绍页与必要工作流改动，保留其他未完成修改。
