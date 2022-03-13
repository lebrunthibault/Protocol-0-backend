// noinspection JSUnresolvedVariable
module.exports = {
  apps: [{
    script: ".\\scripts\\start_midi_server.py",
    watch: ["./api", "./lib"],
    // Delay between restart
    watch_delay: 1000,
    ignore_watch : ["./api/sdk_generation", "*\\__pycache__\\*", "*\\.mypy_cache\\*"],
    stop_exit_codes: [0],
    // autorestart: false
  }]
}
