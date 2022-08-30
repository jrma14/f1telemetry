import { Progress } from "@material-tailwind/react";
import {Link} from "react-router-dom"

function Test() {
    return (
    <div className="flex-col flex w-full h-screen gap-4 items-center">
        <Link to="/">
            <img className="left-2 h-[40px] w-[40px] top-1" src='https://cdn-icons-png.flaticon.com/512/60/60817.png' />
        </Link>
        <Progress value={50} variant="filled" className="w-1/2"/>
        <Progress value={50} variant="gradient" />
    </div>
    )
}

export default Test