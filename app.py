from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
import random
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# Game state management
games = {}
waiting_players = []

class Game:
    def __init__(self, game_id, player1_id, player1_name):
        self.game_id = game_id
        self.players = {
            player1_id: {
                'name': player1_name,
                'choice': None,
                'ready': False,
                'score': {'wins': 0, 'losses': 0, 'ties': 0}
            }
        }
        self.round = 1
        self.max_rounds = 5
        self.status = 'waiting'  # waiting, playing, finished
        self.round_results = []
        self.created_at = datetime.now()

    def add_player(self, player_id, player_name):
        if len(self.players) < 2:
            self.players[player_id] = {
                'name': player_name,
                'choice': None,
                'ready': False,
                'score': {'wins': 0, 'losses': 0, 'ties': 0}
            }
            if len(self.players) == 2:
                self.status = 'playing'
            return True
        return False

    def make_choice(self, player_id, choice):
        if player_id in self.players and self.status == 'playing':
            self.players[player_id]['choice'] = choice
            self.players[player_id]['ready'] = True
            return True
        return False

    def both_ready(self):
        return all(player['ready'] for player in self.players.values())

    def determine_winner(self):
        choices = {pid: player['choice'] for pid, player in self.players.items()}
        player_ids = list(choices.keys())
        
        if len(player_ids) != 2:
            return None
            
        choice1, choice2 = choices[player_ids[0]], choices[player_ids[1]]
        
        if choice1 == choice2:
            return 'tie'
        
        winning_combinations = {
            "rock": "scissors",
            "paper": "rock", 
            "scissors": "paper"
        }
        
        if winning_combinations[choice1] == choice2:
            return player_ids[0]
        else:
            return player_ids[1]

    def process_round(self):
        if not self.both_ready():
            return None
            
        winner = self.determine_winner()
        player_ids = list(self.players.keys())
        
        # Update scores
        if winner == 'tie':
            for pid in player_ids:
                self.players[pid]['score']['ties'] += 1
        elif winner in player_ids:
            winner_name = self.players[winner]['name']
            loser_id = player_ids[1] if winner == player_ids[0] else player_ids[0]
            self.players[winner]['score']['wins'] += 1
            self.players[loser_id]['score']['losses'] += 1
        
        # Store round result
        round_result = {
            'round': self.round,
            'choices': {pid: self.players[pid]['choice'] for pid in player_ids},
            'winner': winner,
            'scores': {pid: self.players[pid]['score'].copy() for pid in player_ids}
        }
        self.round_results.append(round_result)
        
        # Reset choices for next round
        for player in self.players.values():
            player['choice'] = None
            player['ready'] = False
        
        self.round += 1
        
        # Check if game is finished
        if self.round > self.max_rounds:
            self.status = 'finished'
            
        return round_result

def generate_game_id():
    return f"game_{random.randint(1000, 9999)}"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/singleplayer')
def singleplayer():
    if 'score' not in session:
        session['score'] = {'wins': 0, 'losses': 0, 'ties': 0}
    return render_template('index.html', score=session['score'])

@app.route('/multiplayer')
def multiplayer():
    return render_template('multiplayer.html')

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")
    # Remove from waiting list
    if request.sid in waiting_players:
        waiting_players.remove(request.sid)
    
    # Handle game cleanup
    for game_id, game in games.items():
        if request.sid in game.players:
            leave_room(game_id)
            del game.players[request.sid]
            if len(game.players) == 0:
                del games[game_id]
            else:
                emit('player_left', {'message': 'Opponent disconnected'}, room=game_id)

@socketio.on('find_game')
def handle_find_game(data):
    player_name = data.get('player_name', f'Player_{request.sid[:4]}')
    
    if waiting_players:
        # Join existing game
        opponent_id = waiting_players.pop(0)
        game_id = generate_game_id()
        game = Game(game_id, opponent_id, f'Player_{opponent_id[:4]}')
        game.add_player(request.sid, player_name)
        games[game_id] = game
        
        # Join both players to the game room
        join_room(game_id)
        socketio.emit('join_room', {'room': game_id}, room=opponent_id)
        join_room(game_id)
        
        # Notify both players
        emit('game_found', {
            'game_id': game_id,
            'players': list(game.players.values()),
            'status': 'playing'
        }, room=game_id)
        
    else:
        # Wait for opponent
        waiting_players.append(request.sid)
        emit('waiting_for_opponent', {'message': 'Waiting for opponent...'})

@socketio.on('join_room')
def handle_join_room(data):
    room = data.get('room')
    if room:
        join_room(room)

@socketio.on('make_choice')
def handle_make_choice(data):
    game_id = data.get('game_id')
    choice = data.get('choice')
    
    if game_id in games:
        game = games[game_id]
        if game.make_choice(request.sid, choice):
            emit('choice_made', {
                'player': request.sid,
                'choice': choice,
                'ready': True
            }, room=game_id)
            
            # Check if both players are ready
            if game.both_ready():
                round_result = game.process_round()
                if round_result:
                    emit('round_result', round_result, room=game_id)
                    
                    if game.status == 'finished':
                        # Determine final winner
                        final_scores = {pid: player['score'] for pid, player in game.players.items()}
                        emit('game_finished', {
                            'final_scores': final_scores,
                            'round_results': game.round_results
                        }, room=game_id)

@socketio.on('play_again')
def handle_play_again(data):
    game_id = data.get('game_id')
    if game_id in games:
        game = games[game_id]
        game.round = 1
        game.status = 'playing'
        game.round_results = []
        for player in game.players.values():
            player['choice'] = None
            player['ready'] = False
            player['score'] = {'wins': 0, 'losses': 0, 'ties': 0}
        
        emit('game_restarted', {
            'players': list(game.players.values()),
            'status': 'playing'
        }, room=game_id)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, debug=False, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True) 