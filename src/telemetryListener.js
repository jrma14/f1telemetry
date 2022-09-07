class telemetryListener {

    static listener

    constructor(ip,port) {
        this.ip = ip
        this.port = port
        if (!this.listener){
            this.listener = new EventSource(`http://${this.ip}:${this.port}/api/listen`)
        }
    }

    get() {
        return this.listener
    }

}


let listener = new telemetryListener('127.0.0.1',5000)
export default listener