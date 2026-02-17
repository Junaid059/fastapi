from fastapi import WebSocket
from typing import Dict, List


class ConnectionManager:
    """Manages WebSocket connections for real-time chat"""
    
    def __init__(self):
        # Maps user_id to their active WebSocket connections
        self.active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Accept connection and add to active connections"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        print(f"User {user_id} connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        """Remove connection from active connections"""
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        print(f"User {user_id} disconnected. Total connections: {len(self.active_connections)}")
    
    def is_user_online(self, user_id: int) -> bool:
        """Check if a user is currently connected"""
        return user_id in self.active_connections and len(self.active_connections[user_id]) > 0
    
    async def send_personal_message(self, message: dict, user_id: int):
        """Send message to a specific user (all their active connections)"""
        if user_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.append(connection)
            # Clean up dead connections
            for conn in disconnected:
                self.active_connections[user_id].remove(conn)


# Global connection manager instance
manager = ConnectionManager()
