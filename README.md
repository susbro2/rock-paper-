# Rock Paper Scissors Web Game

A beautiful, modern web-based Rock Paper Scissors game built with Flask with both single-player and multiplayer modes.

## Features

- 🎮 Interactive gameplay with smooth animations
- 📊 Real-time score tracking
- 🎨 Modern, responsive UI design
- 📱 Mobile-friendly interface
- 🔄 Session-based score persistence
- 🎯 Simple and intuitive controls
- 🌐 **Real-time multiplayer mode** with live opponents
- ⚡ **WebSocket support** for instant gameplay
- 🏆 **5-round tournament system** in multiplayer
- 👥 **Automatic matchmaking** system

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

## How to Play

### Single Player Mode
1. Go to the main page at `http://localhost:5000`
2. Click on one of the three buttons: 🪨 (Rock), 📄 (Paper), or ✂️ (Scissors)
3. The computer will randomly choose its weapon
4. See who wins and watch your score update!
5. Use the "Reset Score" button to start fresh

### Multiplayer Mode
1. Click the "🎮 Play Multiplayer" button or go to `http://localhost:5000/multiplayer`
2. The system will automatically find an opponent for you
3. Once matched, you'll see both players' scores and status
4. Choose your weapon when it's your turn
5. Play 5 rounds to determine the winner
6. Use "Play Again" to rematch with the same opponent or "Find New Game" for a new opponent

## Game Rules

- **Rock** beats **Scissors**
- **Paper** beats **Rock**
- **Scissors** beats **Paper**
- Same choices result in a tie

## Technology Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Real-time Communication:** Flask-SocketIO, WebSockets
- **Styling:** Modern CSS with gradients and animations
- **Session Management:** Flask sessions
- **Multiplayer Engine:** Socket.IO with eventlet

## Project Structure

```
├── app.py              # Main Flask application with multiplayer support
├── templates/
│   ├── index.html      # Single-player game interface
│   └── multiplayer.html # Multiplayer game interface
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Development

The application uses:
- **Flask** for the web framework
- **Flask-SocketIO** for real-time multiplayer functionality
- **Session management** for score persistence
- **AJAX** for smooth gameplay without page reloads
- **WebSockets** for instant multiplayer communication
- **Responsive design** for mobile compatibility
- **Eventlet** for asynchronous networking

## License

This project is open source and available under the MIT License. 