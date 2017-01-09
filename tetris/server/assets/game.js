Vue.use(VueSocketio.default, 'http://' + document.domain + ':' + location.port + '/game')

var DEFAULT_DATA = function (msg) {
	return {
		messages: msg || [],
		join_room_id: '',
		room_id: '',
		joined_room: false,
		username: '',
		username_set: false,
		board_state: '',
		is_owner: false
	}
}

new Vue({
	el: '#app',
	template: '#app-t',

	created: function () {
		this.$keyboard_event = this.keydown.bind(this)
		window.addEventListener('keydown', this.$keyboard_event)
	},
	destroyed: function () {
		window.removeEventListener('keydown', this.$keyboard_event)
	},

	sockets: {
		connect: function () { this.msg('Connected'); this.reset() },
		disconnect: function () { this.msg('Disconnected') },

		message: function (msg) {
			this.msg(msg)
		},

		'room id': function (id) {
			if(this.joined_room) return;
			this.joined_room = true
			this.room_id = id
			this.msg('Join game room: ' + id)
		},

		'board state': function (state) {
			this.board_state = state
		}
	},

	methods: {
		reset: function () {
			Object.assign(this.$data, DEFAULT_DATA(this.messages))
		},

		msg: function (m) {
			this.messages.unshift(m)
		},

		create_room: function () {
			this.$socket.emit('create room')
			this.is_owner = true
		},

		join_room: function (id) {
			if(!id) {
				this.msg('Can not join room (Invalid ID)')
				return
			}
			this.$socket.emit('join room', id)
		},

		set_username: function (name) {
			this.username_set = true
			this.$socket.emit('set name', name)
		},

		start_game: function () {
			this.$socket.emit('start game')
		},

		keydown: function (e) {
			var op = null

			switch(e.code) {
				case 'Space':
					op = 'BOOM'
					break
				case 'ArrowLeft':
				case 'KeyH':
					op = 'MOVE_LEFT'
					break
				case 'ArrowRight':
				case 'KeyL':
					op = 'MOVE_RIGHT'
					break
				case 'ArrowUp':
				case 'KeyK':
					op = 'ROTATE_RIGHT'
					break
				case 'KeyJ':
					op = 'ROTATE_LEFT'
					break
			}
			if(op) {
				console.log('Fire: ' + op)
				this.$socket.emit('game input', op)
			}
		}
	},

	data: DEFAULT_DATA
})
