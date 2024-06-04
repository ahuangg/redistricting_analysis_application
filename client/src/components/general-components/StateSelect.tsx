import React from "react";
import { Select, SelectItem } from "@tremor/react";

import { states } from "@/constants/stringConstants";

import { useAtom, useSetAtom } from "jotai";
import {
    currStateAtom,
    pageStateAtom,
    ensemblesAtom,
    currEnsembleAtom,
    measureAtom,
    clustersAtom,
} from "@/atoms/atoms";

const StateSelect = () => {
    const setPageState = useSetAtom(pageStateAtom);
    const [currState, setCurrState] = useAtom(currStateAtom);
    const [ensembles, setEnsembles] = useAtom(ensemblesAtom);
    const [currEnsemble, setCurrEnsemble] = useAtom(currEnsembleAtom);
    const [measure, setMeasure] = useAtom(measureAtom);
    const [clusters, setClusters] = useAtom(clustersAtom);

    const handleStateSelect = (state: string) => {
        if (state === "All States") {
            setPageState("MapView");
        } else {
            setPageState("OverView");
        }
        setClusters([]);
        setCurrState(state);
        setEnsembles([]);
        setCurrEnsemble({});
        setMeasure("");
    };

    return (
        <Select
            defaultValue="All States"
            value={currState}
            enableClear={false}
            className="p-0 w-[100px]"
        >
            {states.map((state) => {
                return (
                    <SelectItem
                        key={state}
                        value={state}
                        onClick={() =>
                            state !== currState ? handleStateSelect(state) : ""
                        }
                    >
                        {state}
                    </SelectItem>
                );
            })}
        </Select>
    );
};

export default StateSelect;
