import React from "react"
import { Link } from 'react-router-dom'
import { Button } from "@material-tailwind/react";

function Home(props) {
    return (
        <div className="bg-background min-h-screen min-w-full p-4 text-center items-center flex-col">
            <h1 className="font-bold text-4xl">
                F1 Telemetry
            </h1>
            <div className="flex justify-center items-center h-screen">
                <Link to={"/"}>
                    <Button variant="gradient" color="pink" className="rounded-full">
                        Telemetry
                    </Button>
                </Link>
                <Link to={"/calculator"}>
                    <Button variant="gradient" color="pink" className="ml-5 rounded-full">
                        Difficulty Calculator
                    </Button>
                </Link>
            </div>
        </div>
    )
}

export default Home