![Werewolf Local](docs/readme/banner.png)

# Werewolf Local

[English](README.md) · [简体中文](README.zh-CN.md)

Gather on the same Wi-Fi, open a room, and let the game move from day to night.

[Introduction](https://songhaifan.github.io/frankie-werewolf/) · [Guide](docs/guide.md) · [Run locally](#run-locally)

## What it does

- Host a room on a computer and join from mobile browsers.
- Choose player presets and follow the day/night flow.
- Use the built-in Chinese judge announcements to guide the round.

## Run locally

Install the server and client dependencies, then start both:

```sh
npm ci
npm start
```

Use the frontend URL printed by Vite. Other players connect through the host computer on the same network.

## Before you start

This is a local-network game. Phones need to reach the host computer, and the React client needs its Socket.IO server. Room and setup details are in the project guide.

## For developers

```sh
npm run build --prefix client
```

Check room creation, phone joining and the day/night flow against the local server.

[Project guide](docs/guide.md) · [Artwork](docs/readme/README.md)

---

Made by [Songhai Fan](https://github.com/SonghaiFan) · A Frankie project
