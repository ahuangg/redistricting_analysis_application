import React from "react";
import { Card, ProgressBar } from "@tremor/react";

const Loading = () => {
    return (
        <Card className="p-0 h-[100vh] width-full flex justify-center items-center">
            <ProgressBar value={0} className="mt-3 w-[60%]"></ProgressBar>
        </Card>
    );
};

export default Loading;
