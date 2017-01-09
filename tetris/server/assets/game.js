Vue.use(VueSocketio.default, 'http://' + document.domain + ':' + location.port + '/game')

var DEFAULT_DATA = function (msg) {
	return {
		messages: msg || [],
		join_room_id: '',
		room_id: '',
		joined_room: false,
		username: '',
		username_set: false
	}
}

new Vue({
	el: '#app',
	template: '#app-t',

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
		}
	},

	data: DEFAULT_DATA
})