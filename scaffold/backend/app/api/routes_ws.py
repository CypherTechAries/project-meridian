"""WebSocket endpoint for broadcasting tick updates.

A minimal plain-FastAPI WebSocket (no external broker) that advances a run and streams each
tick's macro snapshot to the client. A production build would swap this for Socket.IO rooms
(python-socketio is already in requirements) so multiple players share a run's stream.
"""

from __future__ import annotations

import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from . import runs

router = APIRouter(tags=["realtime"])


@router.websocket("/ws/runs/{run_id}")
async def tick_stream(websocket: WebSocket, run_id: str) -> None:
    """Stream tick updates for a run.

    Client sends `{"ticks": N}` (or nothing → 1) to advance; server pushes one macro snapshot
    per tick. Closes if the run id is unknown.
    """
    await websocket.accept()
    try:
        model = runs.get_run(run_id)
    except KeyError:
        await websocket.send_json({"error": "run not found"})
        await websocket.close()
        return

    try:
        while True:
            try:
                msg = await websocket.receive_json()
                ticks = int(msg.get("ticks", 1))
            except Exception:
                ticks = 1
            for _ in range(max(1, ticks)):
                model.step()
                await websocket.send_json(
                    {"tick": model.tick, "macro_state": model.macro_snapshot()}
                )
                await asyncio.sleep(0)  # yield to the event loop
    except WebSocketDisconnect:
        return
