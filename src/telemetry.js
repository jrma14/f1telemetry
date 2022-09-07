import { Link } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { Progress, Switch } from '@material-tailwind/react'


function Telemetry() {
    const [telemetry, setTelemetry] = useState({ 'nothing': 'yet' })

    const [throttle, setThrottle] = useState(0)

    const [brake, setBrake] = useState(0)

    const [drs, setDRS] = useState(false)

    const [currentLapTime, setCurrentLapTime] = useState('0')

    useEffect(() => {
        const event = new EventSource("http://localhost:5000/api/listen")

        event.addEventListener("update", e => {
            // try {
            //     console.log(JSON.parse(e.data))
            // }catch (error){
            //     console.log(`Error:${error} \n ${e.data}`)
            // }
            try {
                let temp = JSON.parse(e.data)
                setTelemetry(temp)
                const ind = temp.header.playerCarIndex
                if (temp.packetType === 'Car Telemetry') {
                    setThrottle(temp.carTelemetryData[ind].throttle * 100)
                    setBrake(temp.carTelemetryData[ind].brake * 100)
                    setDRS(temp.carTelemetryData[ind].drs === 1)
                }
                if (temp.packetType === 'Lap data') {
                    console.log(temp)
                    setCurrentLapTime(temp.lapData[ind].currentLapTimeInMS/1000)
                }
            } catch (error) {
                // console.log(error)
                // console.log(e.data)
            }
        }, true)
    }, [])

    // console.log(telemetry)

    return (
        <div className="">
            <div className='flex justify-center'>
                <Link to="/">
                    <img className="left-2 h-[40px] w-[40px] top-1" src='https://cdn-icons-png.flaticon.com/512/60/60817.png' />
                </Link>
            </div>
            <h1 className='text-center'>
                {parseFloat(currentLapTime).toFixed(3)}
            </h1>
            <div className='flex justify-center'>
                <Progress value={throttle} color='green' className='w-1/2' />
            </div>
            <div className='flex justify-center mt-4'>
                <Progress value={brake} color='red' className='w-1/2' />
            </div>
            <div className='flex justify-center mt-4'>
                <Switch checked={drs} />
            </div>
            {/* <h1 className='ml-20 pt-5'>
            {JSON.stringify(telemetry,null,2)}
        </h1> */}
        </div>
    )
}

export default Telemetry