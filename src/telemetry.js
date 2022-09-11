import { Link } from 'react-router-dom'
import { useState, useEffect, useRef } from 'react'
import { Progress, Radio } from '@material-tailwind/react'
import listener from "./telemetryListener"

function Telemetry() {
    const [lapData, setLapData] = useState({})

    const [telemetry, setTelemetry] = useState({})

    const playerCarIndex = useRef(-1)

    useEffect(() => {
        let telemetryListener = listener.get()
        telemetryListener.addEventListener("update", e => {
            try {
                let temp = JSON.parse(e.data)
                // console.log(temp.packetType)
                playerCarIndex.current = temp.header.playerCarIndex
                if (temp.packetType === 'Car Telemetry') {
                    // console.log(temp.carTelemetryData)
                    setTelemetry(temp.carTelemetryData)
                }
                if (temp.packetType === 'Lap data') {
                    setLapData(temp.lapData)
                }
                if (temp.packetType === 'Event'){
                    // console.log(temp)
                    // temp.Message ? console.log(temp.Message):console.log('')
                }
            } catch (error) {
                console.log(error)
                console.log(e.data)
            }
        }, true)
    }, [])
    
    try {
        return (
            <div className="">
                <div className='flex justify-center'>
                    <Link to="/">
                        <img className="left-2 h-[40px] w-[40px] top-1" alt='home button' src='https://cdn-icons-png.flaticon.com/512/60/60817.png' />
                    </Link>
                </div>
                <h1 className='text-center'>
                    {lapData[playerCarIndex.current] ? parseFloat(lapData[playerCarIndex.current].currentLapTimeInMS / 1000).toFixed(3) : 'none'}
                </h1>
                <h1 className='text-center'>
                    {telemetry[playerCarIndex.current] ? parseInt(telemetry[playerCarIndex.current].speed) : 'none'}
                </h1>
                <h1 className='text-center'>
                    {telemetry[playerCarIndex.current] ? parseInt(telemetry[playerCarIndex.current].gear) : 'none'}
                </h1>
                {/* <div> broken on server side
                    {telemetry[playerCarIndex.current]?telemetry[playerCarIndex.current].tyresSurfaceTemperature.map((e) => {return (<h1>{e}</h1>)}):'none'}
                </div> */}
                <div className='flex justify-center'>
                    <Progress value={telemetry[playerCarIndex.current] ? telemetry[playerCarIndex.current].throttle * 100 : 0} color='green' className='w-1/2' />
                </div>
                <div className='flex justify-center mt-4'>
                    <Progress value={telemetry[playerCarIndex.current] ? telemetry[playerCarIndex.current].brake * 100 : 0} color='red' className='w-1/2' />
                </div>
                <div className='flex justify-center mt-4'>
                    <Radio checked={telemetry[playerCarIndex.current] ? telemetry[playerCarIndex.current].drs : 0} color="pink" />
                </div>
                <div className='flex justify-center' id='steeringWheel'>
                    <img src='https://cdn.discordapp.com/attachments/701535716022288436/1017215503888027709/wheel.png' alt='wheel' className={` w-[50px] h-[50px] rotate-[${telemetry[playerCarIndex.current]?Math.round(telemetry[playerCarIndex.current].steer * 180):0}deg]`} />
                </div>
                <h1 className='text-center'>
                {telemetry[playerCarIndex.current]? Math.round(telemetry[playerCarIndex.current].steer * 180):0}
                </h1>
            </div>
        )
    } catch (error) {
        debugger
        console.log(error)
    }
}
export default Telemetry