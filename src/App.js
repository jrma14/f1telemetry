import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import "./App.css";
import Form from "./form"
import Calculator from "./calculator"
import Credits from "./credits";
import Telemetry from "./telemetry"
import Home from "./Home"
import Test from "./test"


// @material-tailwind/react
import { ThemeProvider } from "@material-tailwind/react";

const App = () => {
    const [laptimes, setLaptimes] = useState({})

    // console.log("getting usertimes")

    useEffect(() => {
        fetch("http://localhost:5000/api/getusertimes").then(res => {
            return res.json()
        }).then(data => {
            setLaptimes(data)
        }).catch(err => {
            console.error(err)
        })
    }, [])

    function settime(track, time, diff) {
        laptimes[track.toLowerCase().replace(/ /g, "_")] = {
            laptime: time,
            difficulty: diff,
        }
        setLaptimes(laptimes)
    }

    return (
        <ThemeProvider>
            <Router>
                <Routes>
                    <Route path="/" element={<Telemetry />}/>
                    <Route path="/calculator" element={<Calculator lapTimes={laptimes} setLapTimes={settime} />} />
                    <Route path="/form" element={<Form laptimes={laptimes} setLaptimes={settime} />} />
                    <Route path="/credits" element={<Credits />} />
                    <Route path="/menu" element={<Home />} />
                </Routes>
            </Router>
        </ThemeProvider>

    )
}

export default App